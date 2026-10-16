def slugify(text: str) -> str:
    """Turn a title into a URL-friendly slug.

    Lowercase the text, replace every run of characters that aren't
    a-z or 0-9 with a single hyphen, and strip hyphens from both ends.

    >>> slugify("Hello, World!")
    'hello-world'
    """
    raise NotImplementedError("TODO: implement slugify")
