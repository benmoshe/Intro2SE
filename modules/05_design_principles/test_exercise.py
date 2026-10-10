import json

import pytest


@pytest.fixture
def report(impl):
    return impl.Report(
        title="Scores",
        rows=[{"name": "Ada", "score": 90}, {"name": "Linus", "score": 85}],
    )


@pytest.fixture
def registry(impl):
    registry = impl.ExporterRegistry()
    registry.register("json", impl.JsonExporter())
    registry.register("csv", impl.CsvExporter())
    return registry


def test_json_exporter(impl, report):
    assert json.loads(impl.JsonExporter().export(report)) == {
        "title": "Scores",
        "rows": [{"name": "Ada", "score": 90}, {"name": "Linus", "score": 85}],
    }


def test_csv_exporter(impl, report):
    assert impl.CsvExporter().export(report).splitlines() == [
        "name,score",
        "Ada,90",
        "Linus,85",
    ]


def test_csv_exporter_quotes_values_containing_commas(impl):
    report = impl.Report(title="People", rows=[{"name": "Lovelace, Ada"}])
    assert impl.CsvExporter().export(report).splitlines() == ["name", '"Lovelace, Ada"']


def test_csv_exporter_with_no_rows(impl):
    assert impl.CsvExporter().export(impl.Report(title="Empty", rows=[])) == ""


def test_registry_dispatches_by_format(impl, registry, report):
    assert registry.export(report, "json") == impl.JsonExporter().export(report)
    assert registry.export(report, "csv") == impl.CsvExporter().export(report)


def test_registry_lists_formats_sorted(registry):
    assert registry.formats() == ["csv", "json"]


def test_unknown_format_raises(impl, registry, report):
    with pytest.raises(impl.UnknownFormatError, match="yaml"):
        registry.export(report, "yaml")


def test_new_formats_plug_in_without_changing_the_registry(registry, report):
    class ShoutingTitleExporter:
        def export(self, report):
            return report.title.upper()

    registry.register("shout", ShoutingTitleExporter())

    assert registry.export(report, "shout") == "SCORES"
    assert registry.formats() == ["csv", "json", "shout"]


def test_registries_do_not_share_state(impl):
    first, second = impl.ExporterRegistry(), impl.ExporterRegistry()
    first.register("json", impl.JsonExporter())
    assert second.formats() == []
