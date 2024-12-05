from src.cli import cloud_app


def check_error(exc_info, expect_error_class, expect_error_message):
    error = exc_info[1]
    assert isinstance(error, expect_error_class), (
        f"Mismatch error class: expected {expect_error_class}, "
        f"but got {error.__name__}"
    )
    assert expect_error_message in str(error), (
        f"Mismatch error message: expected '{expect_error_message}' to be part of "
        f"'{error}'"
    )


def test_s3_config_add_new_profile(runner, aws_config_file):
    """Test adding a new AWS profile."""
    result = runner.invoke(
        cloud_app,
        [
            "s3-config",
            "test-profile",
            "us-west-2",
            "test-access-key",
            "test-secret-key",
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


def test_s3_config_existing_profile(runner, aws_config_file):
    """Test attempting to add a duplicate AWS profile."""
    result = runner.invoke(
        cloud_app,
        [
            "s3-config",
            "test-profile1",
            "us-west-2",
            "test-access-key",
            "test-secret-key",
        ],
    )
    assert result.exit_code != 0
    check_error(result.exc_info, ValueError, "already exists")
