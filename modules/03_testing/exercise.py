import time
from collections.abc import Callable


def parse_duration(text: str) -> int:
    """Convert a duration like "1h30m" or "45s" to a number of seconds.

    Units are h, m and s. Each may appear at most once, in that order.
    Anything else raises ValueError.
    """
    raise NotImplementedError("TODO: implement parse_duration")


class RateLimiter:
    """Allow at most `max_calls` calls in any window of `period` seconds.

    A call made at time t stops counting once the clock reaches t + period.
    """

    def __init__(
        self,
        max_calls: int,
        period: float,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        raise NotImplementedError("TODO: store what you need")

    def allow(self) -> bool:
        """Record a call and return True if it's within the limit, else False.

        Rejected calls are not recorded.
        """
        raise NotImplementedError("TODO: implement allow")
