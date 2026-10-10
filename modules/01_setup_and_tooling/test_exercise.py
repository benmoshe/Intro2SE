import pytest


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello World", "hello-world"),
        ("Hello, World!", "hello-world"),
        ("  Clean   Code!! ", "clean-code"),
        ("already-slugged", "already-slugged"),
        ("Python 3.12 rocks", "python-3-12-rocks"),
        ("", ""),
        ("!!!", ""),
    ],
)
def test_slugify(impl, text, expected):
    assert impl.slugify(text) == expected
