from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class RenderCreateRequest(BaseModel):
    code: str = Field(min_length=1, max_length=100_000)
    format: Literal["custom_harness"] = "custom_harness"
    captcha_token: str = Field(default="", max_length=4096)


class RenderCreateResponse(BaseModel):
    job_id: str
    access_token: str
    status: str


class RenderStatusResponse(BaseModel):
    job_id: str
    status: str
    message: Optional[str] = None
    error_message: Optional[str] = None
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    has_video: bool
