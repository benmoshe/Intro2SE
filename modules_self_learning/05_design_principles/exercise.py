from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Report:
    title: str
    rows: list[dict[str, object]]


class Exporter(Protocol):
    def export(self, report: Report) -> str: ...


class UnknownFormatError(ValueError):
    """Raised when no exporter is registered for the requested format."""


class JsonExporter:
    def export(self, report: Report) -> str:
        """Return a JSON object with "title" and "rows" keys."""
        raise NotImplementedError("TODO")


class CsvExporter:
    def export(self, report: Report) -> str:
        """Return CSV: a header line from the first row's keys, then one line per row.

        A report with no rows exports as an empty string. Use the csv module.
        """
        raise NotImplementedError("TODO")


class ExporterRegistry:
    """Maps format names to exporters. New formats are added by registering, not editing."""

    def __init__(self) -> None:
        raise NotImplementedError("TODO")

    def register(self, fmt: str, exporter: Exporter) -> None:
        raise NotImplementedError("TODO")

    def formats(self) -> list[str]:
        """Return the registered format names, sorted."""
        raise NotImplementedError("TODO")

    def export(self, report: Report, fmt: str) -> str:
        """Export with the exporter registered for fmt, or raise UnknownFormatError."""
        raise NotImplementedError("TODO")
