import re


def slugify(text: str) -> str:
    """Turn a title into a URL-friendly slug.

    >>> slugify("Hello, World!")
    'hello-world'
    """
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
