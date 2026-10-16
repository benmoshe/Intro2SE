from __future__ import annotations

import logging
import time
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import TypeVar

T = TypeVar("T")

logger = logging.getLogger(__name__)

# --- Configuration ---

_TRUE = {"1", "true", "yes"}
_FALSE = {"0", "false", "no"}


class ConfigError(Exception):
    """Raised when configuration is missing or invalid."""


@dataclass(frozen=True)
class Config:
    database_url: str
    port: int = 8000
    debug: bool = False


def load_config(env: Mapping[str, str]) -> Config:
    """Build a Config from environment variables, raising ConfigError on any problem."""
    database_url = env.get("APP_DATABASE_URL", "")
    if not database_url:
        raise ConfigError("APP_DATABASE_URL is required")
    return Config(
        database_url=database_url,
        port=_parse_port(env.get("APP_PORT", "8000")),
        debug=_parse_bool(env.get("APP_DEBUG", "false")),
    )


def _parse_port(raw: str) -> int:
    message = f"APP_PORT must be an integer between 1 and 65535, got {raw!r}"
    try:
        port = int(raw)
    except ValueError as error:
        raise ConfigError(message) from error
    if not 1 <= port <= 65535:
        raise ConfigError(message)
    return port


def _parse_bool(raw: str) -> bool:
    value = raw.lower()
    if value in _TRUE:
        return True
    if value in _FALSE:
        return False
    raise ConfigError(f"APP_DEBUG must be one of 1/true/yes/0/false/no, got {raw!r}")


# --- Retrying ---


def retry(
    fn: Callable[[], T],
    *,
    attempts: int = 3,
    delay: float = 0.1,
    exceptions: tuple[type[Exception], ...] = (Exception,),
    sleep: Callable[[float], None] = time.sleep,
) -> T:
    """Call fn until it succeeds, at most `attempts` times, and return its result."""
    if attempts < 1:
        raise ValueError("attempts must be at least 1")

    for attempt in range(1, attempts + 1):
        try:
            return fn()
        except exceptions as error:
            logger.warning("attempt %d/%d failed: %s", attempt, attempts, error)
            if attempt == attempts:
                raise
            sleep(delay * 2 ** (attempt - 1))

    raise AssertionError("unreachable")
