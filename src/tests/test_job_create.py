import os
import pytest


@pytest.mark.parametrize(
    "git_url, version",
    [
        (
            "https://github.com/riverbioinformatics/data-sw-visual-studio-code-server.git",
            "0.0.0",
        ),
        (
            "https://github.com/riverbioinformatics/data-sw-jupyterlab.git",
            "0.0.0",
        ),
        (
            "https://github.com/riverbioinformatics/bioinfor-wf-quality-control-ngs.git",
            "0.0.0",
        ),
        (
            "https://github.com/riverbioinformatics/data-sw-rstudio.git",
            "0.0.0",
        ),
    ],
    ids=[
        "overwrite-ui-job",
        "ui-job",
        "no-ui-job",
        "proxy-location",
    ],
)
def test_create_script(
    request,
    runner,
    cli_app,
    base_dir,
    core_config,
    job_script_dir,
    scratch_dir,
    git_url,
    version,
):
    job_id = request.node.callspec.id
    # Build the CLI command arguments
    cli_args = [
        "job",
        "create",
        "--git",
        git_url,
        "--version",
        version,
        "--job-id",
        job_id,
    ]
    # Run the CLI command
    result = runner.invoke(cli_app, cli_args)

    # Check exit code
    assert result.exit_code == 0

    # Check content of the output file against the expected file
    job_dir = os.path.join(scratch_dir, ".river", "jobs", job_id)
    out_file = os.path.join(job_dir, "job.sh")
    expected_out_file = os.path.join(job_dir, "expected_job.sh")
    with open(expected_out_file, "r") as expected_f, open(out_file, "r") as out_f:
        assert (
            expected_f.read() == out_f.read()
        ), "The output content does not match the expected content."
