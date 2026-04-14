from functools import lru_cache
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    api_prefix: str = "/api"
    frontend_origin: str = "http://localhost:4000"
    supabase_url: str = ""
    supabase_service_role_key: str = ""
    supabase_render_bucket: str = "manim-renders"
    redis_url: str = "redis://localhost:6379/0"
    captcha_secret: str = ""
    allow_insecure_captcha_bypass: bool = True
    manim_runtime_image: str = "manim-visualizer-runtime:latest"
    manim_render_quality: str = "ql"
    manim_render_resolution: str = "1920,1080"
    render_timeout_seconds: int = 120
    render_memory_mb: int = 512
    render_cpus: float = 1.0
    render_signed_url_ttl_seconds: int = 300
    render_retention_hours: int = 24
    rate_limit_window_seconds: int = 900
    rate_limit_max_submissions: int = 5
    active_job_ttl_seconds: int = 1800
    queue_name: str = "manim:render_jobs"
    cleanup_interval_seconds: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("supabase_url")
    @classmethod
    def strip_trailing_slash(cls, value: str) -> str:
        return value.rstrip("/")

    @property
    def is_development(self) -> bool:
        return self.app_env.lower() != "production"

    @property
    def project_root(self) -> Path:
        return Path(__file__).resolve().parents[2]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
