import pytest

# --- Strategy ---


def test_no_discount(impl):
    assert impl.no_discount(80.0) == 80.0


def test_percentage_off(impl):
    assert impl.percentage_off(10)(200.0) == pytest.approx(180.0)
    assert impl.percentage_off(0)(200.0) == pytest.approx(200.0)


def test_fixed_off(impl):
    assert impl.fixed_off(15)(100.0) == pytest.approx(85.0)


def test_fixed_off_never_goes_below_zero(impl):
    assert impl.fixed_off(15)(10.0) == 0.0


def test_best_of_picks_the_lowest_price_for_each_amount(impl):
    pricing = impl.best_of(impl.percentage_off(10), impl.fixed_off(15))
    assert pricing(100.0) == pytest.approx(85.0)  # 15 off beats 10%
    assert pricing(500.0) == pytest.approx(450.0)  # 10% beats 15 off


def test_strategies_compose(impl):
    pricing = impl.best_of(impl.no_discount, impl.best_of(impl.fixed_off(5), impl.fixed_off(1)))
    assert pricing(50.0) == pytest.approx(45.0)


# --- Observer ---


@pytest.fixture
def bus(impl):
    return impl.EventBus()


def test_publish_calls_subscribers_with_the_payload(bus):
    received = []
    bus.subscribe("greeted", received.append)

    bus.publish("greeted", "hello")

    assert received == ["hello"]


def test_publish_returns_number_of_handlers_called(bus):
    bus.subscribe("ping", lambda payload: None)
    bus.subscribe("ping", lambda payload: None)
    assert bus.publish("ping") == 2
    assert bus.publish("nobody-listens") == 0


def test_handlers_run_in_subscription_order(bus):
    calls = []
    bus.subscribe("ping", lambda payload: calls.append("first"))
    bus.subscribe("ping", lambda payload: calls.append("second"))

    bus.publish("ping")

    assert calls == ["first", "second"]


def test_handlers_only_receive_their_own_event(bus):
    received = []
    bus.subscribe("a", received.append)

    bus.publish("b", "not for you")

    assert received == []


def test_unsubscribe_stops_delivery(bus):
    received = []
    unsubscribe = bus.subscribe("ping", received.append)

    bus.publish("ping", 1)
    unsubscribe()
    bus.publish("ping", 2)

    assert received == [1]


def test_unsubscribing_twice_is_harmless(bus):
    unsubscribe = bus.subscribe("ping", lambda payload: None)
    unsubscribe()
    unsubscribe()
    assert bus.publish("ping") == 0


# --- Putting them together ---


def test_checkout_applies_pricing_and_announces_payment(impl, bus):
    receipts = []
    bus.subscribe("order_paid", receipts.append)
    checkout = impl.Checkout(pricing=impl.percentage_off(25), bus=bus)

    assert checkout.pay(200.0) == pytest.approx(150.0)
    assert receipts == [{"amount": pytest.approx(150.0)}]


def test_checkout_needs_no_subscribers(impl, bus):
    checkout = impl.Checkout(pricing=impl.no_discount, bus=bus)
    assert checkout.pay(40.0) == 40.0
