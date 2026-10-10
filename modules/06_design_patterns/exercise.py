from __future__ import annotations

from collections.abc import Callable
from typing import Any

PricingStrategy = Callable[[float], float]
Handler = Callable[[Any], None]

# --- Strategy ---


def no_discount(amount: float) -> float:
    raise NotImplementedError("TODO")


def percentage_off(percent: float) -> PricingStrategy:
    """Return a strategy that takes `percent` percent off."""
    raise NotImplementedError("TODO")


def fixed_off(discount: float) -> PricingStrategy:
    """Return a strategy that subtracts `discount`, never going below zero."""
    raise NotImplementedError("TODO")


def best_of(*strategies: PricingStrategy) -> PricingStrategy:
    """Return a strategy that applies whichever given strategy yields the lowest price."""
    raise NotImplementedError("TODO")


# --- Observer ---


class EventBus:
    def __init__(self) -> None:
        raise NotImplementedError("TODO")

    def subscribe(self, event: str, handler: Handler) -> Callable[[], None]:
        """Register handler for event. Return a function that removes it again."""
        raise NotImplementedError("TODO")

    def publish(self, event: str, payload: Any = None) -> int:
        """Call each handler for event, in subscription order. Return how many ran."""
        raise NotImplementedError("TODO")


# --- Putting them together ---


class Checkout:
    def __init__(self, pricing: PricingStrategy, bus: EventBus) -> None:
        raise NotImplementedError("TODO")

    def pay(self, amount: float) -> float:
        """Apply the pricing strategy, publish "order_paid" with {"amount": final}, return final."""
        raise NotImplementedError("TODO")
