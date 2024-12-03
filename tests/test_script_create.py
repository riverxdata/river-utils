import os
import pytest


@pytest.mark.parametrize(
    "git_url, version, allow_access, job_script, bootstrap_script, expected_output",
    [
        (
            "https://github.com/riverbioinformatics/code_server.git",
            "main",
            True,
            "src/main.sh",
            "src/bootstrap.sh",
            "overwrite_url.sh",
        ),
        (
            "https://github.com/riverbioinformatics/code_server.git",
            "main",
            True,
            "src/main.sh",
            None,
            "access.sh",
        ),
        (
            "https://github.com/riverbioinformatics/code_server.git",
            "main",
            False,
            "src/main.sh",
            None,
            "non-ui.sh",
        ),
    ],
    ids=[
        "overwrite url access job",
        "access job",
        "non-ui job",
    ],
)
def test_generate_script(
    runner,
    cli_app,
    base_dir,
    core_config,
    job_script_dir,
    scratch_dir,
    git_url,
    version,
    allow_access,
    job_script,
    bootstrap_script,
    expected_output,
):
    out_file = os.path.join(scratch_dir, "out.sh")

    # Build the CLI command arguments
    cli_args = [
        "script",
        "create",
        "--git",
        git_url,
        "--version",
        version,
        "--config-file",
        core_config,
        "--tools-dir",
        scratch_dir,
        "--job-script",
        job_script,
        "--output-file",
        out_file,
    ]

    # Conditionally add the --allow-access flag
    if allow_access:
        cli_args.append("--allow-access")

    # Add the bootstrap script if it is provided
    if bootstrap_script:
        cli_args.extend(["--bootstrap-script", bootstrap_script])

    # Run the CLI command
    result = runner.invoke(cli_app, cli_args)

    # Check exit code
    assert result.exit_code == 0

    # Check content of the output file against the expected file
    expected_file_path = os.path.join(job_script_dir, expected_output)
    with open(expected_file_path, "r") as expected_f, open(out_file, "r") as out_f:
        assert (
            expected_f.read() == out_f.read()
        ), "The output content does not match the expected content."
