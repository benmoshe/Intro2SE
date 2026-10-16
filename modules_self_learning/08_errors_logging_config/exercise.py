from __future__ import annotations

import logging
import time
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import TypeVar

T = TypeVar("T")

logger = logging.getLogger(__name__)

# --- Configuration ---


class ConfigError(Exception):
    """Raised when configuration is missing or invalid."""


@dataclass(frozen=True)
class Config:
    database_url: str
    port: int = 8000
    debug: bool = False


def load_config(env: Mapping[str, str]) -> Config:
    """Build a Config from environment variables.

    APP_DATABASE_URL  required, non-empty
    APP_PORT          optional integer from 1 to 65535 (default 8000)
    APP_DEBUG         optional; 1/true/yes or 0/false/no, any case (default false)

    Raise ConfigError, with a message naming the variable, for anything else.
    """
    raise NotImplementedError("TODO")


# --- Retrying ---


def retry(
    fn: Callable[[], T],
    *,
    attempts: int = 3,
    delay: float = 0.1,
    exceptions: tuple[type[Exception], ...] = (Exception,),
    sleep: Callable[[float], None] = time.sleep,
) -> T:
    """Call fn until it succeeds, at most `attempts` times, and return its result.

    When fn raises one of `exceptions`: log a warning, then, if attempts remain,
    sleep before trying again — `delay` after the first failure, doubling each time.
    After the final failed attempt, re-raise its exception without sleeping.

    Exceptions not listed in `exceptions` propagate immediately.
    Raise ValueError if attempts is less than 1.
    """
    raise NotImplementedError("TODO")
