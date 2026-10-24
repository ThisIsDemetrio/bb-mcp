import os


class ConfigError(RuntimeError):
    pass


def load() -> dict:
    """Read settings from the environment; fail fast on anything unusable."""
    mode = os.environ.get("BB_MODE", "local")
    if mode != "local":
        raise ConfigError(
            f"BB_MODE={mode!r} is not supported yet; only 'local' is implemented"
        )
    pat = os.environ.get("BB_PAT", "")
    if not pat.startswith("bbpat_"):
        raise ConfigError(
            "BB_PAT must be set to a personal token starting with 'bbpat_'"
        )
    return {
        "pat": pat,
        "base_url": os.environ.get(
            "BB_API_BASE_URL", "https://sb1-api.buzzerbeater.com/v1"
        ),
        "log_level": os.environ.get("LOG_LEVEL", "INFO").upper(),
    }
