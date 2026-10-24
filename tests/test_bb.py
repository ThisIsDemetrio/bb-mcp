import asyncio

import pytest
from fastmcp import Client

from bb_mcp import config
from bb_mcp.api import to_error
from bb_mcp.app import mcp


def test_error_mapping():
    assert "new personal token" in str(to_error(401, "InvalidToken", "x"))
    assert "00:00 UTC" in str(to_error(429, "PublicApiQuotaExceeded", "x"))
    assert "Request failed (404)" in str(to_error(404, "NewUnknownCode", "x"))
    assert "try again" in str(to_error(503, "Retry", "x"))


def test_config(monkeypatch):
    monkeypatch.delenv("BB_PAT", raising=False)
    with pytest.raises(config.ConfigError):
        config.load()
    monkeypatch.setenv("BB_PAT", "bbpat_x")
    assert config.load()["pat"] == "bbpat_x"
    monkeypatch.setenv("BB_MODE", "hosted")
    with pytest.raises(config.ConfigError):
        config.load()


def test_tools_registered_and_read_only(monkeypatch):
    import bb_mcp.tools  # noqa: F401

    async def go():
        async with Client(mcp) as c:
            return await c.list_tools()

    monkeypatch.setenv("BB_PAT", "bbpat_x")
    tools = asyncio.run(go())
    assert len(tools) == 29  # one per GET path
    assert all(t.annotations and t.annotations.read_only_hint for t in tools)


def test_get_retries_burst_429_once(monkeypatch):
    import httpx

    from bb_mcp import api

    calls = []

    def handler(req):
        calls.append(req)
        if len(calls) == 1:
            return httpx.Response(
                429, headers={"Retry-After": "0"}, json={"code": "RateLimited"}
            )
        return httpx.Response(200, json={"ok": True})

    async def go():
        async with httpx.AsyncClient(
            base_url="http://x/v1/", transport=httpx.MockTransport(handler)
        ) as api.client:
            return await api.get("teams/1", flag=True, skip=None, types=["A", "B"])

    assert asyncio.run(go()) == {"ok": True}
    assert len(calls) == 2
    assert str(calls[0].url) == "http://x/v1/teams/1?flag=true&types=A&types=B"
