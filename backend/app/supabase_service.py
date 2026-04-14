from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from supabase import Client, create_client

from app.config import Settings


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class SupabaseService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client: Client = create_client(settings.supabase_url, settings.supabase_service_role_key)

    def create_job(self, payload: dict[str, Any]) -> dict[str, Any]:
        response = self.client.table("manim_jobs").insert(payload).execute()
        rows = response.data or []
        if not rows:
            raise RuntimeError("Supabase did not return the inserted render job.")
        return rows[0]

    def get_job(self, job_id: str) -> dict[str, Any] | None:
        response = self.client.table("manim_jobs").select("*").eq("id", job_id).limit(1).execute()
        rows = response.data or []
        return rows[0] if rows else None

    def update_job(self, job_id: str, payload: dict[str, Any]) -> dict[str, Any] | None:
        response = self.client.table("manim_jobs").update(payload).eq("id", job_id).execute()
        rows = response.data or []
        return rows[0] if rows else None

    def delete_job(self, job_id: str) -> None:
        self.client.table("manim_jobs").delete().eq("id", job_id).execute()

    def list_expired_jobs(self) -> list[dict[str, Any]]:
        response = (
            self.client.table("manim_jobs")
            .select("*")
            .lt("expires_at", utcnow().isoformat())
            .neq("status", "expired")
            .limit(100)
            .execute()
        )
        rows = response.data or []
        return [row for row in rows if row.get("status") in {"completed", "failed"}]

    def list_purgeable_expired_jobs(self) -> list[dict[str, Any]]:
        threshold = utcnow() - timedelta(hours=self.settings.render_retention_hours)
        response = (
            self.client.table("manim_jobs")
            .select("id")
            .eq("status", "expired")
            .lt("expires_at", threshold.isoformat())
            .limit(100)
            .execute()
        )
        return response.data or []

    def storage_path_for_job(self, job_id: str) -> str:
        return f"renders/{job_id}/output.mp4"

    def upload_video(self, storage_path: str, file_path: Path) -> None:
        with file_path.open("rb") as file_handle:
            self.client.storage.from_(self.settings.supabase_render_bucket).upload(
                storage_path,
                file_handle,
                {"content-type": "video/mp4", "x-upsert": "true"},
            )

    def remove_video(self, storage_path: str) -> None:
        self.client.storage.from_(self.settings.supabase_render_bucket).remove([storage_path])

    def create_signed_video_url(self, storage_path: str) -> str:
        payload = self.client.storage.from_(self.settings.supabase_render_bucket).create_signed_url(
            storage_path,
            self.settings.render_signed_url_ttl_seconds,
        )

        signed_url = payload.get("signedURL") or payload.get("signedUrl") or payload.get("signed_url")
        if not signed_url:
            raise RuntimeError("Supabase did not return a signed URL for the rendered MP4.")

        if signed_url.startswith("http://") or signed_url.startswith("https://"):
            return signed_url

        if not signed_url.startswith("/"):
            signed_url = f"/{signed_url}"

        return f"{self.settings.supabase_url}/storage/v1{signed_url}"


_supabase_service: SupabaseService | None = None


def get_supabase_service(settings: Settings) -> SupabaseService:
    global _supabase_service

    if _supabase_service is None:
        _supabase_service = SupabaseService(settings)

    return _supabase_service
