import pytest
from river.cli import cloud_app


def check_error(exc_info, expect_error_class, expect_error_message):
    error = exc_info[1]
    assert isinstance(error, expect_error_class), (
        f"Mismatch error class: expected {expect_error_class}, "
        f"but got {type(error).__name__}"
    )
    assert expect_error_message in str(error), (
        f"Mismatch error message: expected '{expect_error_message}' to be part of "
        f"'{str(error)}'"
    )


@pytest.fixture
def aws_config_file(tmp_path, monkeypatch):
    config_dir = tmp_path / ".aws"
    config_dir.mkdir()
    config_file = config_dir / "config"
    monkeypatch.setenv("HOME", str(tmp_path))
    return config_file


def test_s3_config_add_new_profile_no_url(runner, aws_config_file):
    result = runner.invoke(
        cloud_app,
        [
            "--profile-name",
            "test-profile-no-url",
            "--region",
            "us-west-2",
            "--aws-access-key-id",
            "test-access-key",
            "--aws-secret-access-key",
            "test-secret-key",
        ],
    )
    assert result.exit_code == 0
    assert "Profile 'test-profile-no-url' successfully added" in result.output
    with open(aws_config_file) as f:
        content = f.read()
        assert "[test-profile-no-url]" in content
        assert "region = us-west-2" in content
        assert "aws_access_key_id = test-access-key" in content
        assert "aws_secret_access_key = test-secret-key" in content
        assert "endpoint_url" not in content


def test_s3_config_add_new_profile(runner, aws_config_file):
    result = runner.invoke(
        cloud_app,
        [
            "--profile-name",
            "test-profile",
            "--region",
            "us-west-2",
            "--aws-access-key-id",
            "test-access-key",
            "--aws-secret-access-key",
            "test-secret-key",
            "--endpoint-url",
            "http://localhost:9000",
        ],
    )
    assert result.exit_code == 0
    assert "Profile 'test-profile' successfully added" in result.output
    with open(aws_config_file) as f:
        content = f.read()
        assert "[test-profile]" in content
        assert "region = us-west-2" in content
        assert "aws_access_key_id = test-access-key" in content
        assert "aws_secret_access_key = test-secret-key" in content
        assert "endpoint_url = http://localhost:9000" in content


def test_s3_config_existing_profile(runner, aws_config_file):
    with open(aws_config_file, "w") as f:
        f.write("[test-profile]\nregion = us-west-2\n")
    result = runner.invoke(
        cloud_app,
        [
            "--profile-name",
            "test-profile",
            "--region",
            "us-west-2",
            "--aws-access-key-id",
            "test-access-key",
            "--aws-secret-access-key",
            "test-secret-key",
        ],
    )
    assert result.exit_code != 0
    check_error(result.exc_info, ValueError, "already exists")


def test_s3_config_missing_region(runner, aws_config_file):
    result = runner.invoke(
        cloud_app,
        [
            "--profile-name",
            "test-profile",
            "--aws-access-key-id",
            "test-access-key",
            "--aws-secret-access-key",
            "test-secret-key",
        ],
    )
    assert result.exit_code != 0
    check_error(result.exc_info, SystemExit, "2")
