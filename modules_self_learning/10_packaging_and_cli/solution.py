from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Counts:
    lines: int
    words: int
    chars: int


def count(text: str) -> Counts:
    """Count lines, whitespace-separated words, and characters. Pure: no I/O."""
    return Counts(lines=len(text.splitlines()), words=len(text.split()), chars=len(text))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="wordcount",
        description="Count lines, words and characters in files.",
    )
    parser.add_argument("files", nargs="+", metavar="FILE", help="files to count")
    parser.add_argument("-l", "--lines", action="store_true", help="print the line count")
    parser.add_argument("-w", "--words", action="store_true", help="print the word count")
    parser.add_argument("-c", "--chars", action="store_true", help="print the character count")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    show_all = not (args.lines or args.words or args.chars)
    exit_code = 0

    for name in args.files:
        try:
            counts = count(Path(name).read_text())
        except OSError as error:
            print(f"wordcount: {name}: {error.strerror}", file=sys.stderr)
            exit_code = 1
            continue

        columns: list[object] = []
        if show_all or args.lines:
            columns.append(counts.lines)
        if show_all or args.words:
            columns.append(counts.words)
        if show_all or args.chars:
            columns.append(counts.chars)
        print(*columns, name)

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
