import asyncio
from typing import Any

import httpx
from fastmcp.exceptions import ToolError

client: httpx.AsyncClient | None = None
MAX_WAIT = 30

HINT_MAP = {
    "PublicApiQuotaExceeded": "Daily call quota used up; wait for the reset at 00:00 UTC.",
    "PublicApiBreadthExceeded": "Foreign-resource budget reached; already read resources still work.",
    "PublicApiListedSkillsExceeded": "Listed-skills reveal limit reached; check the auction in the game.",
}


def to_error(status: int, code: str | None, description: str | None) -> ToolError:
    """Map a BuzzerBeater error response to a ToolError. 429 errors have hint defined in HINT_MAP"""
    detail = f"{description or 'no description'} ({code or 'no code'})"
    if status == 401:
        return ToolError(
            f"Token rejected: {detail}. Create a new personal token in the game and update BB_PAT."
        )
    if status == 403:
        return ToolError(
            f"Not allowed: {detail}. The token lacks a scope, or the resource is not yours."
        )
    if status == 429:
        hint = HINT_MAP.get(code or "", "Rate limited.")
        return ToolError(f"{hint} {detail}")
    if status >= 500:
        return ToolError(f"BuzzerBeater server problem, try again later: {detail}")
    return ToolError(f"Request failed ({status}): {detail}")


def _clean(params: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k, v in params.items():
        if v is None:
            continue
        out[k] = str(v).lower() if isinstance(v, bool) else v
    return out


async def get(path: str, **params: Any) -> Any:
    assert client is not None, "server not started"

    for attempt in (0, 1):
        try:
            r = await client.get(path, params=_clean(params))
        except httpx.HTTPError as e:
            raise ToolError(
                f"Network error talking to BuzzerBeater: {type(e).__name__}"
            ) from None
        if r.status_code < 400:
            return r.json()

        try:
            body = r.json()
        except ValueError:
            body = {}

        code = body.get("code")

        if r.status_code == 429 and code == "RateLimited" and attempt == 0:
            await asyncio.sleep(min(float(r.headers.get("Retry-After", 1)), MAX_WAIT))
            continue

        raise to_error(r.status_code, code, body.get("description"))
