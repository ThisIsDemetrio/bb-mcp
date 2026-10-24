from typing import Literal

from ..api import get
from ..app import RO, mcp


@mcp.tool(annotations=RO)
async def get_player(player_id: str) -> dict:
    """
    Player page. Includes only public information (age, name, potential, game shape, DMI, etc) and skills only for your own players.
    """
    return await get(f"players/{player_id}")


@mcp.tool(annotations=RO)
async def get_player_training(
    player_id: str, sort: Literal["Asc", "Desc"] | None = None
) -> dict:
    """Training sessions of your own player. Require a supporter subscription, or info won't be returned to you."""
    return await get(f"players/{player_id}/training", sort=sort)
