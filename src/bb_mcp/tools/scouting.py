from typing import Literal

from ..api import get
from ..app import RO, mcp

MatchType = Literal[
    "Scrimmage",
    "League",
    "PrivateLeague",
    "Madness",
    "Best",
    "World",
    "Continental",
    "Cup",
    "Consolation",
    "Pickup",
    "AllStar",
]


@mcp.tool(annotations=RO)
async def scout_team(
    team_id: str,
    match_types: list[MatchType],
    locations: list[Literal["Home", "Away", "Neutral"]],
    last_games: int | None = None,
    season: int | None = None,
) -> dict:
    """Scout a club's tactics over its recent games. Use only when explicitly asked to scout a team.
    Give `last_games` (1-30, default 10) OR `season`, not both.
    Some information might require a supporter subscription.
    """
    return await get(
        f"teams/{team_id}/scouting",
        matchTypes=match_types,
        locations=locations,
        lastGames=last_games,
        season=season,
    )


@mcp.tool(annotations=RO)
async def get_match_shooting(match_id: str) -> dict:
    """Shot zones and per-player attempts for a finished match. Use only when explicitly asked for a detailed analysis of a team."""
    return await get(f"matches/{match_id}/shooting")
