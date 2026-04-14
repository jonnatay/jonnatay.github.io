import httpx

from app.config import Settings


TURNSTILE_VERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"


async def verify_captcha(token: str, ip_address: str, settings: Settings) -> bool:
    if not settings.captcha_secret:
        return settings.allow_insecure_captcha_bypass and settings.is_development

    if not token:
        return False

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(
            TURNSTILE_VERIFY_URL,
            data={
                "secret": settings.captcha_secret,
                "response": token,
                "remoteip": ip_address,
            },
        )
        response.raise_for_status()
        payload = response.json()
        return bool(payload.get("success"))
