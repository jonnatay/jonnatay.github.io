import hashlib
import hmac
import secrets
from typing import Optional

from fastapi import Header, Query, Request


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def generate_access_token() -> str:
    return secrets.token_urlsafe(32)


def verify_hash(candidate: str, expected_hash: str) -> bool:
    return hmac.compare_digest(sha256_text(candidate), expected_hash)


def get_request_ip(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for", "")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    if request.client and request.client.host:
        return request.client.host

    return "unknown"


def hash_submitter_identifier(ip_address: str) -> str:
    return sha256_text(ip_address)


def access_token_input(
    access_token: Optional[str] = Query(default=None),
    x_access_token: Optional[str] = Header(default=None, alias="X-Access-Token"),
) -> str:
    return access_token or x_access_token or ""
