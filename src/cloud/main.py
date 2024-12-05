import os
import typer

cloud_app = typer.Typer(
    help="""
A Command Line Interface (CLI) tool for managing S3 configurations and mounting S3 buckets using Goofys.

Commands:
- `s3-config`: Add a new AWS profile to your local configuration.
- `s3-mount`: Mount an S3 bucket using Goofys.
- `s3-umount`: Unmount a mounted S3 bucket.
"""
)


@cloud_app.command(name="s3-config", help="Add a new AWS profile to ~/.aws/config.")
def s3_config(
    profile_name: str = typer.Option(
        ..., "--profile-name", help="AWS profile name to add."
    ),
    region: str = typer.Option(..., "--region", help="AWS region (e.g., us-west-2)."),
    aws_access_key_id: str = typer.Option(
        ..., "--aws-access-key-id", help="Your AWS access key ID."
    ),
    aws_secret_access_key: str = typer.Option(
        ..., "--aws-secret-access-key", help="Your AWS secret access key."
    ),
    endpoint_url: str = typer.Option(
        None, "--endpoint-url", help="Optional custom AWS endpoint URL."
    ),
):
    """
    Add a new AWS profile to ~/.aws/config.
    """
    aws_config_file = os.path.expanduser("~/.aws/config")
    aws_dir = os.path.dirname(aws_config_file)
    os.makedirs(aws_dir, exist_ok=True)

    if os.path.exists(aws_config_file):
        with open(aws_config_file, "r") as config_file:
            if f"[{profile_name}]" in config_file.read():
                raise ValueError(
                    f"Profile '{profile_name}' already exists in {aws_config_file}."
                )

    print(f"Adding profile '{profile_name}' to AWS config...")
    with open(aws_config_file, "a") as config_file:
        config_file.write(
            f"\n[{profile_name}]\n"
            f"region = {region}\n"
            f"aws_access_key_id = {aws_access_key_id}\n"
            f"aws_secret_access_key = {aws_secret_access_key}\n"
        )
        if endpoint_url:
            config_file.write(f"endpoint_url = {endpoint_url}\n")

    print(f"Profile '{profile_name}' successfully added to {aws_config_file}.")
