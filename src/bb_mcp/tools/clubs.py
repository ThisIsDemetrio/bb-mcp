from typing import Literal

from ..api import get
from ..app import RO, mcp


@mcp.tool(annotations=RO)
async def get_team(team_id: str) -> dict:
    """A summary of a club: name, country, manager, league, arena, record."""
    return await get(f"teams/{team_id}")


@mcp.tool(annotations=RO)
async def get_team_roster(team_id: str) -> dict:
    """
    Give the complete roster of a team. For your own team, you also get the skill values, otherwise
    you'll get only the public information (name, age, DMI, game shape)
    """
    return await get(f"teams/{team_id}/roster")


@mcp.tool(annotations=RO)
async def get_team_schedule(
    team_id: str,
    season: int | None = None,
    offset: int | None = None,
    limit: int | None = None,
) -> dict:
    """A club schedule, oldest info come first."""
    return await get(
        f"teams/{team_id}/schedule", season=season, offset=offset, limit=limit
    )


@mcp.tool(annotations=RO)
async def get_team_stats(
    team_id: str,
    season: int | None = None,
    mode: Literal["Averages", "Totals"] | None = None,
) -> dict:
    """Team statistics for a season. You can get more details with \"mode\" parameter equal to \"Totals\"."""
    return await get(f"teams/{team_id}/stats", season=season, mode=mode)


@mcp.tool(annotations=RO)
async def get_team_arena(team_id: str) -> dict:
    """Public information about a team arena (seats and prices)."""
    return await get(f"teams/{team_id}/arena")
