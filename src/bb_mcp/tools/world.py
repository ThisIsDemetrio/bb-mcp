from ..api import get
from ..app import RO, mcp


@mcp.tool(annotations=RO)
async def get_standings(competition_id: str, season: int | None = None) -> dict:
    """Standings table per group of each stage of a BuzzerBeater competition."""
    return await get(f"competitions/{competition_id}/standings", season=season)


@mcp.tool(annotations=RO)
async def get_seasons(offset: int | None = None, limit: int | None = None) -> dict:
    """Seasons, oldest first."""
    return await get("seasons", offset=offset, limit=limit)


@mcp.tool(annotations=RO)
async def get_countries() -> dict:
    """Every country available in BuzzerBeater."""
    return await get("countries")


@mcp.tool(annotations=RO)
async def get_country_leagues(
    country_id: str,
    level: int | None = None,
    division: int | None = None,
    offset: int | None = None,
    limit: int | None = None,
) -> dict:
    """Leagues of a country. `level` is zero-based (0 = top), `division` one-based (1 = top); if both are given they must agree."""
    return await get(
        f"countries/{country_id}/leagues",
        level=level,
        division=division,
        offset=offset,
        limit=limit,
    )


@mcp.tool(annotations=RO)
async def get_country_national_teams(country_id: str) -> dict:
    """Senior and junior national teams of a country, with coaches."""
    return await get(f"countries/{country_id}/national-teams")


@mcp.tool(annotations=RO)
async def get_national_team_roster(team_id: str) -> dict:
    """Called-up squad of a national team. Skills only for the coach."""
    return await get(f"national-teams/{team_id}/roster")


@mcp.tool(annotations=RO)
async def get_national_team_training_history(
    team_id: str, offset: int | None = None, limit: int | None = None
) -> dict:
    """
    Squad skill changes from club training of players included in a National team, newest first.
    Works only for coaches/assistant of said national team, otherwise the request will fail.
    """
    return await get(
        f"national-teams/{team_id}/training/history", offset=offset, limit=limit
    )
