from __future__ import annotations

import csv
import io
import json
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
        return json.dumps({"title": report.title, "rows": report.rows})


class CsvExporter:
    def export(self, report: Report) -> str:
        if not report.rows:
            return ""
        buffer = io.StringIO()
        writer = csv.DictWriter(buffer, fieldnames=list(report.rows[0]))
        writer.writeheader()
        writer.writerows(report.rows)
        return buffer.getvalue()


class ExporterRegistry:
    """Maps format names to exporters. New formats are added by registering, not editing."""

    def __init__(self) -> None:
        self._exporters: dict[str, Exporter] = {}

    def register(self, fmt: str, exporter: Exporter) -> None:
        self._exporters[fmt] = exporter

    def formats(self) -> list[str]:
        return sorted(self._exporters)

    def export(self, report: Report, fmt: str) -> str:
        try:
            exporter = self._exporters[fmt]
        except KeyError:
            raise UnknownFormatError(f"no exporter registered for {fmt!r}") from None
        return exporter.export(report)
