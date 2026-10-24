from contextlib import asynccontextmanager

import httpx
from fastmcp import FastMCP

from . import api, config

INSTRUCTIONS = """\
Read-only wrapper around the BuzzerBeater public API. Call get_me first to learn your team ids and granted scopes. \
Own-club tools (training, staff, facilities, economy) need the matching token scope; \
other clubs return 403. Generally speaking prefer few, targeted calls and do not crawl other clubs or players. \
Useful for analyzing the roster of your own team (to suggest tactics and training plans) and other teams (for scouting \
or counter-tactics), for analyzing players for sale and how they fit in your roster, or get generic information about \
teams, players, national teams and everything related to BuzzerBeater.
"""


@asynccontextmanager
async def lifespan(_server):
    cfg = config.load()
    async with httpx.AsyncClient(
        base_url=cfg["base_url"].rstrip("/") + "/",
        headers={"Authorization": f"Bearer {cfg['pat']}"},
        timeout=30,
    ) as api.client:
        yield


mcp = FastMCP("bb-mcp", instructions=INSTRUCTIONS, lifespan=lifespan)
RO = {"readOnlyHint": True}
