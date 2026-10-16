from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from typing import Any

PricingStrategy = Callable[[float], float]
Handler = Callable[[Any], None]

# --- Strategy ---


def no_discount(amount: float) -> float:
    return amount


def percentage_off(percent: float) -> PricingStrategy:
    """Return a strategy that takes `percent` percent off."""

    def apply(amount: float) -> float:
        return amount * (1 - percent / 100)

    return apply


def fixed_off(discount: float) -> PricingStrategy:
    """Return a strategy that subtracts `discount`, never going below zero."""

    def apply(amount: float) -> float:
        return max(amount - discount, 0.0)

    return apply


def best_of(*strategies: PricingStrategy) -> PricingStrategy:
    """Return a strategy that applies whichever given strategy yields the lowest price."""

    def apply(amount: float) -> float:
        return min(strategy(amount) for strategy in strategies)

    return apply


# --- Observer ---


class EventBus:
    def __init__(self) -> None:
        self._handlers: defaultdict[str, list[Handler]] = defaultdict(list)

    def subscribe(self, event: str, handler: Handler) -> Callable[[], None]:
        """Register handler for event. Return a function that removes it again."""
        self._handlers[event].append(handler)

        def unsubscribe() -> None:
            if handler in self._handlers[event]:
                self._handlers[event].remove(handler)

        return unsubscribe

    def publish(self, event: str, payload: Any = None) -> int:
        """Call each handler for event, in subscription order. Return how many ran."""
        # Copy so a handler that unsubscribes mid-publish doesn't skip its neighbour.
        handlers = list(self._handlers.get(event, ()))
        for handler in handlers:
            handler(payload)
        return len(handlers)


# --- Putting them together ---


class Checkout:
    def __init__(self, pricing: PricingStrategy, bus: EventBus) -> None:
        self._pricing = pricing
        self._bus = bus

    def pay(self, amount: float) -> float:
        final = self._pricing(amount)
        self._bus.publish("order_paid", {"amount": final})
        return final
