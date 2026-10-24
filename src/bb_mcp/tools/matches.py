from ..api import get
from ..app import RO, mcp


@mcp.tool(annotations=RO)
async def get_match(match_id: str, include_boxscore: bool = False) -> dict:
    """Match header: teams, date, competition, score by period. Box score is not included until the match is overnds."""
    return await get(
        f"matches/{match_id}", include="boxscore" if include_boxscore else None
    )


@mcp.tool(annotations=RO)
async def get_boxscore(match_id: str) -> dict:
    """Box score: strategies, ratings, every player's line. Can be received only after the match is over."""
    return await get(f"matches/{match_id}/boxscore")


@mcp.tool(annotations=RO)
async def get_match_events(match_id: str, cursor: int | None = None) -> dict:
    """
    One page (up to 200) of play-by-play for a finished match.
    Request is paginated with a cursor, pass `nextCursor` from the result for the next page.
    Use it only when the user request it or to get a detailed recap or analysis of a game.
    """
    return await get(f"matches/{match_id}/events", cursor=cursor)
