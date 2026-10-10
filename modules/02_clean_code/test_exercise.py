import pytest

ITEMS = [
    {"price": 30.0, "quantity": 2},
    {"price": 50.0, "quantity": 1},
]


# --- Behaviour: these pass before you start and must keep passing. ---


@pytest.mark.parametrize(
    ("tier", "expected"),
    [
        ("regular", 118.80),  # 110, free shipping, 8% tax
        ("silver", 112.91),  # 99 after 10% off, + tax + shipping
        ("gold", 101.03),  # 88 after 20% off, + tax + shipping
    ],
)
def test_order_total_by_tier(impl, tier, expected):
    assert impl.order_total({"items": ITEMS, "tier": tier}) == pytest.approx(expected)


def test_order_total_of_empty_order_is_just_shipping(impl):
    assert impl.order_total({"items": [], "tier": "regular"}) == pytest.approx(5.99)


def test_order_of_exactly_100_still_pays_shipping(impl):
    order = {"items": [{"price": 100.0, "quantity": 1}], "tier": "regular"}
    assert impl.order_total(order) == pytest.approx(113.99)


# --- Structure: these fail until you extract the helpers. ---


def test_subtotal(impl):
    assert impl.subtotal(ITEMS) == pytest.approx(110.0)
    assert impl.subtotal([]) == 0


@pytest.mark.parametrize(
    ("tier", "rate"),
    [("gold", 0.2), ("silver", 0.1), ("regular", 0.0), ("unknown", 0.0)],
)
def test_discount_rate(impl, tier, rate):
    assert impl.discount_rate(tier) == pytest.approx(rate)


@pytest.mark.parametrize(
    ("amount", "cost"),
    [(0, 5.99), (100, 5.99), (100.01, 0.0), (500, 0.0)],
)
def test_shipping_cost(impl, amount, cost):
    assert impl.shipping_cost(amount) == pytest.approx(cost)
