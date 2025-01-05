import json


def test_get_job_state(
    request,
    runner,
    cli_app,
    base_dir,
):
    # clean if install
    cli_args = ["job", "info", "uuid"]
    result = runner.invoke(cli_app, cli_args)
    assert result.exit_code == 0
    assert json.loads(result.output.strip("\n")) == {
        "uuid_job_id": "uuid",
        "slurm_job_id": "1",
        "proxy_location": "uuid/",
        "url": "uuid",
        "port": "localhost",
        "host": "localhost",
    }
