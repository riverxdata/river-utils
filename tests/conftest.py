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


@pytest.fixture(scope="module")
def aws_config_file():
    config_path = os.path.expanduser("~/.aws/config")
    os.makedirs(os.path.dirname(config_path), exist_ok=True)

    with open(config_path, "w") as config:
        config.write(
            f"[test-profile1]\nregion = {os.environ.get('REGION_NAME')}\naws_access_key_id = {os.environ.get('AWS_ACCESS_KEY_ID')}\naws_secret_access_key = {os.environ.get('AWS_SECRET_ACCESS_KEY')}"
        )

    yield config_path

    if os.path.exists(config_path):
        os.remove(config_path)
