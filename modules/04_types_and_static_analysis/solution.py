from __future__ import annotations

from collections.abc import Callable, Hashable, Iterable
from dataclasses import dataclass
from decimal import Decimal
from typing import TypeVar

T = TypeVar("T")
K = TypeVar("K", bound=Hashable)


class CurrencyMismatch(ValueError):
    """Raised when combining Money values of different currencies."""


@dataclass(frozen=True)
class Money:
    cents: int
    currency: str = "USD"

    @classmethod
    def from_str(cls, text: str, currency: str = "USD") -> Money:
        """Parse a decimal string such as "12.34" or "5" into Money."""
        return cls(int(Decimal(text) * 100), currency)

    def __add__(self, other: Money) -> Money:
        if other.currency != self.currency:
            raise CurrencyMismatch(f"cannot add {self.currency} and {other.currency}")
        return Money(self.cents + other.cents, self.currency)

    def __str__(self) -> str:
        return f"{self.cents // 100}.{self.cents % 100:02d} {self.currency}"


def group_by(items: Iterable[T], key: Callable[[T], K]) -> dict[K, list[T]]:
    """Group items into a dict of lists, keyed by key(item)."""
    groups: dict[K, list[T]] = {}
    for item in items:
        groups.setdefault(key(item), []).append(item)
    return groups
