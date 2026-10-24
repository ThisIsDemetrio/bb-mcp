from typing import Literal

from ..api import get
from ..app import RO, mcp

Sort = Literal["Asc", "Desc"] | None


@mcp.tool(annotations=RO)
async def get_team_training(team_id: str) -> dict:
    """Current training drill and positions of your own team."""
    return await get(f"teams/{team_id}/training")


@mcp.tool(annotations=RO)
async def get_team_training_history(
    team_id: str, offset: int | None = None, limit: int | None = None, sort: Sort = None
) -> dict:
    """Results of past training sessions (skill upgrades and such) of your own team. Non-supporters get the latest session only."""
    return await get(
        f"teams/{team_id}/training/history", offset=offset, limit=limit, sort=sort
    )


@mcp.tool(annotations=RO)
async def get_team_staff(team_id: str) -> dict:
    """Staff in your own team: role, level, specialty, salary."""
    return await get(f"teams/{team_id}/staff")


@mcp.tool(annotations=RO)
async def get_team_facilities(team_id: str) -> dict:
    """Building available for your own team: levels, max level and weekly upkeep."""
    return await get(f"teams/{team_id}/facilities")


@mcp.tool(annotations=RO)
async def get_team_economy(team_id: str, sort: Sort = None) -> dict:
    """Economy recap of your own team. Balance, available money, expected sale proceeds and transactions."""
    return await get(f"teams/{team_id}/economy", sort=sort)


@mcp.tool(annotations=RO)
async def get_team_salaries(team_id: str) -> dict:
    """Weekly player and staff salaries of your own team."""
    return await get(f"teams/{team_id}/economy/salaries")


@mcp.tool(annotations=RO)
async def get_arena_attendance(
    team_id: str, offset: int | None = None, limit: int | None = None
) -> dict:
    """Info about your own arena. Attendance, prices and gate revenue, newest first."""
    return await get(f"teams/{team_id}/arena/attendance", offset=offset, limit=limit)
