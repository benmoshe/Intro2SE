from __future__ import annotations

import argparse
from dataclasses import dataclass


@dataclass(frozen=True)
class Counts:
    lines: int
    words: int
    chars: int


def count(text: str) -> Counts:
    """Count lines, whitespace-separated words, and characters. Pure: no I/O."""
    raise NotImplementedError("TODO")


def build_parser() -> argparse.ArgumentParser:
    """Build the parser: one or more FILES, plus -l/--lines, -w/--words, -c/--chars."""
    raise NotImplementedError("TODO")


def main(argv: list[str] | None = None) -> int:
    """Print the requested counts for each file to stdout, one file per line.

    Format: the selected counts in the order lines, words, chars, then the
    file name, separated by single spaces. With no flags, all three are shown.

    For a file that can't be read, print "wordcount: <name>: <reason>" to
    stderr and continue. Return 1 if any file failed, otherwise 0.
    """
    raise NotImplementedError("TODO")


if __name__ == "__main__":
    raise SystemExit(main())
