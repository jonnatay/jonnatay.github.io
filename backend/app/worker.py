from __future__ import annotations

import asyncio
import logging
from datetime import datetime

from app.config import get_settings
from app.redis_queue import dequeue_render_job, get_redis_client, release_active_job_slot
from app.render_runner import cleanup_render_result, run_render_job
from app.supabase_service import get_supabase_service, utcnow


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger("manim-worker")


def _truncate_log(value: str | None, max_length: int = 50_000) -> str | None:
    if value is None:
        return None

    if len(value) <= max_length:
        return value

    return value[:max_length] + "\n\n[truncated]"


def _parse_timestamp(value: str | None) -> datetime | None:
    if not value:
        return None

    return datetime.fromisoformat(value.replace("Z", "+00:00"))


async def cleanup_expired_jobs() -> None:
    settings = get_settings()
    supabase = get_supabase_service(settings)

    for job in supabase.list_expired_jobs():
        try:
            if job.get("storage_path"):
                supabase.remove_video(job["storage_path"])
            supabase.update_job(
                job["id"],
                {
                    "status": "expired",
                    "storage_path": None,
                    "message": "Render expired and was cleaned up.",
                },
            )
        except Exception:
            logger.exception("Failed to expire render job %s", job["id"])

    for job in supabase.list_purgeable_expired_jobs():
        try:
            supabase.delete_job(job["id"])
        except Exception:
            logger.exception("Failed to purge expired render job %s", job["id"])


async def process_job(job_id: str) -> None:
    settings = get_settings()
    supabase = get_supabase_service(settings)
    redis_client = await get_redis_client(settings)
    job = supabase.get_job(job_id)
    result = None

    if not job:
        logger.warning("Received unknown job id %s from the queue.", job_id)
        return

    try:
        expires_at = _parse_timestamp(job.get("expires_at"))
        if expires_at and expires_at <= utcnow():
            supabase.update_job(
                job_id,
                {
                    "status": "expired",
                    "message": "Render expired before processing started.",
                },
            )
            return

        supabase.update_job(
            job_id,
            {
                "status": "running",
                "started_at": utcnow().isoformat(),
                "message": "Worker picked up the render and started processing.",
            },
        )

        result = run_render_job(job_id, job["source_code"], settings)

        if result.success and result.output_path:
            storage_path = supabase.storage_path_for_job(job_id)
            supabase.upload_video(storage_path, result.output_path)
            supabase.update_job(
                job_id,
                {
                    "status": "completed",
                    "message": "Render complete. MP4 uploaded successfully.",
                    "storage_path": storage_path,
                    "stdout_log": _truncate_log(result.stdout_log),
                    "stderr_log": _truncate_log(result.stderr_log),
                    "runtime_ms": result.runtime_ms,
                    "output_bytes": result.output_bytes,
                    "completed_at": utcnow().isoformat(),
                    "error_message": None,
                },
            )
            logger.info("Completed render job %s", job_id)
        else:
            supabase.update_job(
                job_id,
                {
                    "status": "failed",
                    "message": "Render failed.",
                    "error_message": result.error_message,
                    "stdout_log": _truncate_log(result.stdout_log),
                    "stderr_log": _truncate_log(result.stderr_log),
                    "runtime_ms": result.runtime_ms,
                    "output_bytes": result.output_bytes,
                    "completed_at": utcnow().isoformat(),
                },
            )
            logger.warning("Render job %s failed: %s", job_id, result.error_message)

    except Exception as error:
        logger.exception("Unexpected worker failure while processing %s", job_id)
        supabase.update_job(
            job_id,
            {
                "status": "failed",
                "message": "Worker crashed while handling this render job.",
                "error_message": str(error),
                "completed_at": utcnow().isoformat(),
            },
        )
    finally:
        if result is not None:
            cleanup_render_result(result)
        await release_active_job_slot(redis_client, job["submitter_hash"])


async def work_forever() -> None:
    settings = get_settings()
    redis_client = await get_redis_client(settings)
    cleanup_deadline = 0.0

    while True:
        now = asyncio.get_running_loop().time()
        if now >= cleanup_deadline:
            await cleanup_expired_jobs()
            cleanup_deadline = now + settings.cleanup_interval_seconds

        job_id = await dequeue_render_job(redis_client, settings, timeout_seconds=5)
        if not job_id:
            continue

        await process_job(job_id)


def main() -> None:
    asyncio.run(work_forever())


if __name__ == "__main__":
    main()
