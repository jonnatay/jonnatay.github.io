from redis.asyncio import Redis

from app.config import Settings


_redis_client: Redis | None = None


async def get_redis_client(settings: Settings) -> Redis:
    global _redis_client

    if _redis_client is None:
        _redis_client = Redis.from_url(settings.redis_url, decode_responses=True)

    return _redis_client


async def enqueue_render_job(redis_client: Redis, settings: Settings, job_id: str) -> None:
    await redis_client.lpush(settings.queue_name, job_id)


async def dequeue_render_job(redis_client: Redis, settings: Settings, timeout_seconds: int = 10) -> str | None:
    result = await redis_client.brpop(settings.queue_name, timeout=timeout_seconds)
    if not result:
        return None

    _, job_id = result
    return job_id


async def consume_rate_limit(redis_client: Redis, settings: Settings, submitter_hash: str) -> int:
    key = f"manim:rate:{submitter_hash}"
    count = await redis_client.incr(key)
    if count == 1:
        await redis_client.expire(key, settings.rate_limit_window_seconds)
    return int(count)


async def acquire_active_job_slot(redis_client: Redis, settings: Settings, submitter_hash: str) -> bool:
    key = f"manim:active:{submitter_hash}"
    result = await redis_client.set(key, "1", ex=settings.active_job_ttl_seconds, nx=True)
    return bool(result)


async def release_active_job_slot(redis_client: Redis, submitter_hash: str) -> None:
    key = f"manim:active:{submitter_hash}"
    await redis_client.delete(key)
