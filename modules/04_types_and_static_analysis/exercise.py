from __future__ import annotations


class CurrencyMismatch(ValueError):
    """Raised when combining Money values of different currencies."""


# TODO: make this a frozen dataclass with fields
#   cents: int
#   currency: str = "USD"
# and delete the placeholder __init__.
class Money:
    def __init__(self, cents, currency="USD"):
        raise NotImplementedError("TODO: turn Money into a frozen dataclass")

    @classmethod
    def from_str(cls, text, currency="USD"):
        """Parse a decimal string such as "12.34" or "5" into Money."""
        raise NotImplementedError("TODO: implement from_str")

    def __add__(self, other):
        raise NotImplementedError("TODO: implement __add__")

    def __str__(self):
        """Format as e.g. "12.34 USD"."""
        raise NotImplementedError("TODO: implement __str__")


# TODO: annotate this so mypy knows the key and item types of the result.
def group_by(items, key):
    """Group items into a dict of lists, keyed by key(item).

    Keys appear in first-seen order; items keep their original order.

    >>> group_by(["apple", "avocado", "banana"], key=lambda s: s[0])
    {'a': ['apple', 'avocado'], 'b': ['banana']}
    """
    raise NotImplementedError("TODO: implement group_by")
