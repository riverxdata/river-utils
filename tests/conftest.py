import pytest
from typer.testing import CliRunner
from src.cli import app
import os


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def cli_app():
    return app


@pytest.fixture
def base_dir():
    return os.path.dirname(__file__)


@pytest.fixture
def scratch_dir(base_dir):
    return os.path.join(base_dir, "scratch")


@pytest.fixture
def data_dir(base_dir):
    return os.path.join(base_dir, "data")


@pytest.fixture
def job_script_dir(data_dir):
    return os.path.join(data_dir, "job")


@pytest.fixture
def core_config(data_dir):
    return os.path.join(data_dir, "config", "core.json")
