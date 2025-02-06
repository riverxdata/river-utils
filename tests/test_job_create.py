import os


def test_create_script(
    request,
    runner,
    cli_app,
    base_dir,
    core_config,
    job_script_dir,
    scratch_dir,
):
    job_id = "job-id"
    # Build the CLI command arguments
    cli_args = [
        "job",
        "create",
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
