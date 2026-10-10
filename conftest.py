"""Shared pytest setup: loads each module's exercise.py (or solution.py) as `impl`."""

import importlib.util
import sys

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--solutions",
        action="store_true",
        help="run the tests against solution.py instead of exercise.py",
    )


@pytest.fixture(scope="module")
def impl(request):
    """The code under test for the module the current test file lives in."""
    name = "solution" if request.config.getoption("--solutions") else "exercise"
    path = request.path.parent / f"{name}.py"
    module_name = f"m{path.parent.name}_{name}"

    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module  # dataclasses look the module up by name
    spec.loader.exec_module(module)
    return module
