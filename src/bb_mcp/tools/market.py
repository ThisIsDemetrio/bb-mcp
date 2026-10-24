from typing import Any, Literal

from fastmcp.exceptions import ToolError

from ..api import get
from ..app import RO, mcp

_SKILLS = [
    "JumpShot",
    "JumpRange",
    "OutsideDefense",
    "Handling",
    "Driving",
    "Passing",
    "InsideShot",
    "InsideDefense",
    "Rebound",
    "ShotBlock",
    "FreeThrow",
]
_RANGED = [
    "Age",
    "Height",
    "Salary",
    "Price",
    "Overall",
    "Potential",
    "Experience",
    "GameShape",
    *_SKILLS,
]
_FILTERS = {f"{p}{n}" for n in _RANGED for p in ("Min", "Max")} | {
    "Country",
    "Position",
    "SecondPosition",
    "Injury",
    "OnNationalTeam",
}


@mcp.tool(annotations=RO)
async def search_market_players(
    filters: dict[str, Any] | None = None,
    order_by: str | None = None,
    sort: Literal["Asc", "Desc"] | None = None,
    offset: int | None = None,
    limit: int | None = None,
) -> dict:
    """
    Search the transfer list with players currently on sale. It does not returns skills, but only public
    information. Use to scout the market and get a glimpse of what could be a good player(s) based on the request
    made. More details of a single player can be received via tool get_auction.

    filters keys (PascalCase): Min/Max + Age, Height, Salary, Price, Overall, Potential, Experience, GameShape,
    JumpShot, JumpRange, OutsideDefense, Handling, Driving, Passing, InsideShot, InsideDefense, Rebound, ShotBlock,
    FreeThrow; plus Country, Position, SecondPosition, Injury (Nothing|OnlyInjured|ExcludeInjured), OnNationalTeam.
    Level-valued filters (skills, Experience, GameShape) take names like Average, Strong, Prolific, Legendary.
    More than four skill bounds needs a supporter; eight is the maximum. order_by e.g. AuctionTime, Age, Salary,
    CurrentBid, Overall, Potential. Searches go at most 150 deep, up to 30 per page.
    """
    # TODO: add the list of levels (text - if values are not used)
    bad = set(filters or {}) - _FILTERS
    if bad:
        raise ToolError(f"Unknown filter(s): {sorted(bad)}")
    return await get(
        "market/players",
        **(filters or {}),
        OrderBy=order_by,
        Sort=sort,
        Offset=offset,
        Limit=limit,
    )


@mcp.tool(annotations=RO)
async def get_auction(player_id: str) -> dict:
    """
    Auction of a listed player. Includes more details then what received with search_market_players, including player skills.
    Use it when the user asks for a player on sale and to compare it with the current people in team.
    Avoid to abuse of this call for crawling for players. Better filter with search_market_players first in case.
    """
    return await get(f"market/players/{player_id}/auction")
