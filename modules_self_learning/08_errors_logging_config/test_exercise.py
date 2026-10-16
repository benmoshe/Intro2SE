import logging

import pytest

# --- load_config ---


def test_minimal_config_uses_defaults(impl):
    config = impl.load_config({"APP_DATABASE_URL": "sqlite:///app.db"})
    assert config == impl.Config(database_url="sqlite:///app.db", port=8000, debug=False)


def test_full_config(impl):
    config = impl.load_config(
        {"APP_DATABASE_URL": "postgres://db/app", "APP_PORT": "5000", "APP_DEBUG": "true"}
    )
    assert config == impl.Config(database_url="postgres://db/app", port=5000, debug=True)


def test_unrelated_variables_are_ignored(impl):
    config = impl.load_config({"APP_DATABASE_URL": "x", "HOME": "/root", "PORT": "1"})
    assert config.port == 8000


@pytest.mark.parametrize("env", [{}, {"APP_DATABASE_URL": ""}])
def test_database_url_is_required(impl, env):
    with pytest.raises(impl.ConfigError, match="APP_DATABASE_URL"):
        impl.load_config(env)


@pytest.mark.parametrize("port", ["abc", "", "0", "-1", "65536", "80.5"])
def test_invalid_port_is_rejected(impl, port):
    with pytest.raises(impl.ConfigError, match="APP_PORT"):
        impl.load_config({"APP_DATABASE_URL": "x", "APP_PORT": port})


@pytest.mark.parametrize("port", ["1", "65535"])
def test_port_boundaries_are_accepted(impl, port):
    assert impl.load_config({"APP_DATABASE_URL": "x", "APP_PORT": port}).port == int(port)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("1", True),
        ("true", True),
        ("TRUE", True),
        ("Yes", True),
        ("0", False),
        ("false", False),
        ("No", False),
    ],
)
def test_debug_flag_parsing(impl, raw, expected):
    assert impl.load_config({"APP_DATABASE_URL": "x", "APP_DEBUG": raw}).debug is expected


@pytest.mark.parametrize("raw", ["maybe", "", "2", "on"])
def test_invalid_debug_flag_is_rejected(impl, raw):
    with pytest.raises(impl.ConfigError, match="APP_DEBUG"):
        impl.load_config({"APP_DATABASE_URL": "x", "APP_DEBUG": raw})


def test_config_is_immutable(impl):
    config = impl.load_config({"APP_DATABASE_URL": "x"})
    with pytest.raises(AttributeError):
        config.port = 1


# --- retry ---


class Flaky:
    """Fails a set number of times with the given error, then returns "ok"."""

    def __init__(self, failures, error=None):
        self.failures = failures
        self.error = error or ConnectionError("network down")
        self.calls = 0

    def __call__(self):
        self.calls += 1
        if self.calls <= self.failures:
            raise self.error
        return "ok"


@pytest.fixture
def sleeps():
    """A list that records every requested sleep instead of actually sleeping."""
    return []


def warnings_in(caplog):
    return [record for record in caplog.records if record.levelno == logging.WARNING]


def test_returns_immediately_on_success(impl, sleeps, caplog):
    fn = Flaky(failures=0)

    assert impl.retry(fn, sleep=sleeps.append) == "ok"

    assert fn.calls == 1
    assert sleeps == []
    assert warnings_in(caplog) == []


def test_retries_until_success(impl, sleeps):
    fn = Flaky(failures=2)

    assert impl.retry(fn, attempts=3, sleep=sleeps.append) == "ok"

    assert fn.calls == 3


def test_backs_off_exponentially_between_attempts(impl, sleeps):
    fn = Flaky(failures=3)

    impl.retry(fn, attempts=4, delay=0.5, sleep=sleeps.append)

    assert sleeps == pytest.approx([0.5, 1.0, 2.0])


def test_reraises_the_last_error_when_attempts_run_out(impl, sleeps):
    fn = Flaky(failures=10)

    with pytest.raises(ConnectionError, match="network down"):
        impl.retry(fn, attempts=3, delay=0.1, sleep=sleeps.append)

    assert fn.calls == 3
    assert sleeps == pytest.approx([0.1, 0.2])  # no pointless sleep after the final failure


def test_logs_a_warning_for_each_failed_attempt(impl, sleeps, caplog):
    with caplog.at_level(logging.WARNING):
        impl.retry(Flaky(failures=2), attempts=3, sleep=sleeps.append)

    warnings = warnings_in(caplog)
    assert len(warnings) == 2
    assert "network down" in warnings[0].getMessage()


def test_unlisted_exceptions_propagate_without_retrying(impl, sleeps):
    fn = Flaky(failures=5, error=KeyError("bug"))

    with pytest.raises(KeyError):
        impl.retry(fn, attempts=3, exceptions=(ConnectionError,), sleep=sleeps.append)

    assert fn.calls == 1
    assert sleeps == []


def test_only_listed_exceptions_are_retried(impl, sleeps):
    fn = Flaky(failures=1, error=TimeoutError("slow"))

    assert impl.retry(fn, exceptions=(TimeoutError,), sleep=sleeps.append) == "ok"
    assert fn.calls == 2


def test_attempts_must_be_positive(impl):
    with pytest.raises(ValueError):
        impl.retry(lambda: "ok", attempts=0)
