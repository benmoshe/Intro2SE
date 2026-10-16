import re
import time
from collections import deque
from collections.abc import Callable

_DURATION = re.compile(r"(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?")


def parse_duration(text: str) -> int:
    """Convert a duration like "1h30m" or "45s" to a number of seconds."""
    match = _DURATION.fullmatch(text)
    if not text or match is None:
        raise ValueError(f"invalid duration: {text!r}")
    hours, minutes, seconds = (int(group or 0) for group in match.groups())
    return hours * 3600 + minutes * 60 + seconds


class RateLimiter:
    """Allow at most `max_calls` calls in any window of `period` seconds."""

    def __init__(
        self,
        max_calls: int,
        period: float,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._max_calls = max_calls
        self._period = period
        self._clock = clock
        self._calls: deque[float] = deque()

    def allow(self) -> bool:
        now = self._clock()
        while self._calls and now - self._calls[0] >= self._period:
            self._calls.popleft()
        if len(self._calls) >= self._max_calls:
            return False
        self._calls.append(now)
        return True
