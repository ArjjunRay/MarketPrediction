import json
from collections.abc import Mapping

from redis.asyncio import Redis


class LiveStateStore:
    """Ephemeral latest-state access; never an authoritative history store."""

    def __init__(self, redis: Redis, namespace: str = "qstream") -> None:
        self._redis = redis
        self._namespace = namespace

    def _key(self, category: str, symbol: str) -> str:
        return f"{self._namespace}:{category}:{symbol.upper()}"

    async def set_latest(
        self, category: str, symbol: str, value: Mapping[str, object], ttl_seconds: int = 60
    ) -> None:
        await self._redis.set(self._key(category, symbol), json.dumps(dict(value)), ex=ttl_seconds)

    async def get_latest(self, category: str, symbol: str) -> dict[str, object] | None:
        raw = await self._redis.get(self._key(category, symbol))
        if raw is None:
            return None
        parsed = json.loads(raw)
        if not isinstance(parsed, dict):
            return None
        return parsed
