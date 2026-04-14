from __future__ import annotations

from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.captcha import verify_captcha
from app.config import Settings, get_settings
from app.redis_queue import (
    acquire_active_job_slot,
    consume_rate_limit,
    enqueue_render_job,
    get_redis_client,
)
from app.schemas import RenderCreateRequest, RenderCreateResponse, RenderStatusResponse
from app.security import (
    access_token_input,
    generate_access_token,
    get_request_ip,
    hash_submitter_identifier,
    sha256_text,
    verify_hash,
)
from app.supabase_service import get_supabase_service, utcnow


app = FastAPI(title="Manim Visualizer API", version="1.0.0")


@app.on_event("startup")
async def startup_event() -> None:
    settings = get_settings()
    get_supabase_service(settings)
    await get_redis_client(settings)


settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin, "http://localhost:4000", "http://127.0.0.1:4000"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


def build_status_response(job: dict) -> RenderStatusResponse:
    return RenderStatusResponse(
        job_id=job["id"],
        status=job["status"],
        message=job.get("message"),
        error_message=job.get("error_message"),
        created_at=job.get("created_at"),
        completed_at=job.get("completed_at"),
        expires_at=job.get("expires_at"),
        has_video=bool(job.get("storage_path") and job.get("status") == "completed"),
    )


async def authorize_job(job_id: str, access_token: str, settings: Settings) -> dict:
    if not access_token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Render job not found.")

    supabase = get_supabase_service(settings)
    job = supabase.get_job(job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Render job not found.")

    if not verify_hash(access_token, job["access_token_hash"]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Render job not found.")

    return job


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.post(f"{settings.api_prefix}/renders", response_model=RenderCreateResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_render(
    payload: RenderCreateRequest,
    request: Request,
    settings: Settings = Depends(get_settings),
) -> RenderCreateResponse:
    if payload.format != "custom_harness":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only the custom_harness format is supported.")

    ip_address = get_request_ip(request)
    submitter_hash = hash_submitter_identifier(ip_address)

    if not await verify_captcha(payload.captcha_token, ip_address, settings):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CAPTCHA verification failed.")

    redis_client = await get_redis_client(settings)
    submission_count = await consume_rate_limit(redis_client, settings, submitter_hash)
    if submission_count > settings.rate_limit_max_submissions:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Submission limit exceeded for this time window.",
        )

    active_slot = await acquire_active_job_slot(redis_client, settings, submitter_hash)
    if not active_slot:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Only one active render job is allowed at a time for this client.",
        )

    access_token = generate_access_token()
    now = utcnow()
    expires_at = now + timedelta(hours=settings.render_retention_hours)

    job_payload = {
        "access_token_hash": sha256_text(access_token),
        "status": "queued",
        "format": payload.format,
        "source_code": payload.code,
        "submitter_hash": submitter_hash,
        "message": "Render queued and waiting for a worker.",
        "expires_at": expires_at.isoformat(),
    }

    supabase = get_supabase_service(settings)
    job = None

    try:
        job = supabase.create_job(job_payload)
        await enqueue_render_job(redis_client, settings, job["id"])
    except Exception as error:
        await redis_client.delete(f"manim:active:{submitter_hash}")
        if job:
            supabase.update_job(
                job["id"],
                {
                    "status": "failed",
                    "message": "The job could not be queued for processing.",
                    "error_message": str(error),
                    "completed_at": utcnow().isoformat(),
                },
            )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Render queue is unavailable: {error}",
        ) from error

    return RenderCreateResponse(job_id=job["id"], access_token=access_token, status=job["status"])


@app.get(f"{settings.api_prefix}/renders/{{job_id}}", response_model=RenderStatusResponse)
async def get_render_status(
    job_id: str,
    access_token: str = Depends(access_token_input),
    settings: Settings = Depends(get_settings),
) -> RenderStatusResponse:
    job = await authorize_job(job_id, access_token, settings)
    return build_status_response(job)


@app.get(f"{settings.api_prefix}/renders/{{job_id}}/video")
async def get_render_video(
    job_id: str,
    access_token: str = Depends(access_token_input),
    settings: Settings = Depends(get_settings),
) -> RedirectResponse:
    job = await authorize_job(job_id, access_token, settings)

    if job["status"] != "completed" or not job.get("storage_path"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Render output is not available.")

    signed_url = get_supabase_service(settings).create_signed_video_url(job["storage_path"])
    return RedirectResponse(url=signed_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
