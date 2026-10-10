import dataclasses

import pytest

# --- Money ---


def test_money_defaults_to_usd(impl):
    assert impl.Money(500).currency == "USD"


def test_money_with_equal_values_is_equal(impl):
    assert impl.Money(1234, "EUR") == impl.Money(1234, "EUR")
    assert impl.Money(1234, "EUR") != impl.Money(1234, "USD")


def test_money_is_immutable(impl):
    money = impl.Money(100)
    with pytest.raises(dataclasses.FrozenInstanceError):
        money.cents = 999


def test_money_is_hashable(impl):
    assert len({impl.Money(100), impl.Money(100), impl.Money(200)}) == 2


@pytest.mark.parametrize(
    ("text", "cents"),
    [("12.34", 1234), ("5", 500), ("0.10", 10), ("0.1", 10), ("19.99", 1999)],
)
def test_money_from_str(impl, text, cents):
    assert impl.Money.from_str(text) == impl.Money(cents)


def test_money_from_str_with_currency(impl):
    assert impl.Money.from_str("7.50", "GBP") == impl.Money(750, "GBP")


def test_money_addition_returns_new_money(impl):
    a, b = impl.Money(1050), impl.Money(250)
    assert a + b == impl.Money(1300)
    assert a == impl.Money(1050)


def test_money_addition_has_no_float_error(impl):
    assert impl.Money.from_str("0.10") + impl.Money.from_str("0.20") == impl.Money.from_str("0.30")


def test_adding_different_currencies_raises(impl):
    with pytest.raises(impl.CurrencyMismatch):
        impl.Money(100, "USD") + impl.Money(100, "EUR")


@pytest.mark.parametrize(
    ("cents", "text"),
    [(1234, "12.34 USD"), (500, "5.00 USD"), (5, "0.05 USD"), (0, "0.00 USD")],
)
def test_money_str(impl, cents, text):
    assert str(impl.Money(cents)) == text


# --- group_by ---


def test_group_by_groups_items_under_their_key(impl):
    words = ["apple", "avocado", "banana", "blueberry", "cherry"]
    assert impl.group_by(words, key=lambda word: word[0]) == {
        "a": ["apple", "avocado"],
        "b": ["banana", "blueberry"],
        "c": ["cherry"],
    }


def test_group_by_keeps_first_seen_key_order(impl):
    assert list(impl.group_by([3, 1, 4, 1, 5, 9, 2, 6], key=lambda n: n % 2)) == [1, 0]


def test_group_by_accepts_any_iterable(impl):
    assert impl.group_by((n for n in range(4)), key=lambda n: n < 2) == {
        True: [0, 1],
        False: [2, 3],
    }


def test_group_by_of_nothing_is_empty(impl):
    assert impl.group_by([], key=len) == {}
