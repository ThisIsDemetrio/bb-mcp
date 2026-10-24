from ..api import get
from ..app import RO, mcp


@mcp.tool(annotations=RO)
async def get_me() -> dict:
    """Current manager: username, supporter flag, owned clubs, coached national teams, granted scopes. Start here for team ids."""
    return await get("me")
