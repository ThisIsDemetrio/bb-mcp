import logging

from . import config, tools  # noqa: F401  (importing tools registers the @mcp.tool functions)
from .app import mcp


def main() -> None:
    logging.basicConfig(
        level=config.load()["log_level"]
    )  # stderr; stdout is the MCP channel

    for name in ("httpx", "httpcore"):
        logging.getLogger(name).setLevel(logging.WARNING)

    mcp.run()


if __name__ == "__main__":
    main()
