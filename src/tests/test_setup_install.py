def test_setup_install(
    request,
    runner,
    cli_app,
    base_dir,
):
    # clean if install
    cli_args = ["setup", "clean"]
    result = runner.invoke(cli_app, cli_args)
    assert result.exit_code == 0

    # install
    cli_args = ["setup", "install"]
    result = runner.invoke(cli_app, cli_args)
    assert result.exit_code == 0

    # Check exit code
    cli_args = ["setup", "install"]
    result = runner.invoke(cli_app, cli_args)
    assert result.exit_code == 0
