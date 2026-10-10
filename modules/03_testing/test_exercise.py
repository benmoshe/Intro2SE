import pytest

# --- parse_duration ---


@pytest.mark.parametrize(
    ("text", "seconds"),
    [
        ("45s", 45),
        ("2m", 120),
        ("2h", 7200),
        ("90m", 5400),
        ("1h30m", 5400),
        ("1h2m3s", 3723),
        ("1h5s", 3605),
    ],
)
def test_parse_duration(impl, text, seconds):
    assert impl.parse_duration(text) == seconds


@pytest.mark.parametrize("text", ["", "abc", "10", "1x", "m5", "1h1h", "30m1h", "1.5h", "-5s"])
def test_parse_duration_rejects_invalid_input(impl, text):
    with pytest.raises(ValueError):
        impl.parse_duration(text)


# --- RateLimiter ---


class FakeClock:
    """A clock the test moves by hand, so no test ever has to sleep."""

    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


@pytest.fixture
def clock():
    return FakeClock()


def test_allows_calls_up_to_the_limit(impl, clock):
    limiter = impl.RateLimiter(max_calls=3, period=10, clock=clock)
    assert [limiter.allow() for _ in range(3)] == [True, True, True]


def test_rejects_calls_over_the_limit(impl, clock):
    limiter = impl.RateLimiter(max_calls=2, period=10, clock=clock)
    limiter.allow()
    limiter.allow()
    assert limiter.allow() is False


def test_allows_again_once_the_period_has_passed(impl, clock):
    limiter = impl.RateLimiter(max_calls=1, period=10, clock=clock)
    assert limiter.allow() is True
    clock.now = 9.9
    assert limiter.allow() is False
    clock.now = 10
    assert limiter.allow() is True


def test_window_slides_rather_than_resetting(impl, clock):
    limiter = impl.RateLimiter(max_calls=2, period=10, clock=clock)
    assert limiter.allow() is True  # t=0
    clock.now = 6
    assert limiter.allow() is True  # t=6
    clock.now = 9
    assert limiter.allow() is False  # 0 and 6 both still in the window
    clock.now = 10
    assert limiter.allow() is True  # 0 has expired; window holds 6, 10
    clock.now = 11
    assert limiter.allow() is False
    clock.now = 16
    assert limiter.allow() is True  # 6 has expired


def test_rejected_calls_do_not_count_against_the_limit(impl, clock):
    limiter = impl.RateLimiter(max_calls=1, period=10, clock=clock)
    limiter.allow()
    clock.now = 5
    assert limiter.allow() is False
    clock.now = 10
    assert limiter.allow() is True  # would be False if the t=5 call had been recorded
