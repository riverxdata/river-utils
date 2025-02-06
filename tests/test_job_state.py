import json


def test_get_job_state(
    request,
    runner,
    cli_app,
    base_dir,
):
    # clean if install
    cli_args = ["job", "info", "job-id"]
    result = runner.invoke(cli_app, cli_args)
    assert result.exit_code == 0
    assert json.loads(result.output.strip("\n")) == {
        "uuid_job_id": "job-id",
        "slurm_job_id": "1",
        "proxy_location": "job-id/",
        "url": "job-id",
        "port": "8000",
        "host": "localhost",
    }
