import os
import subprocess
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


def ensure_goofys_installed():
    """Check if Goofys is installed on the system."""
    try:
        subprocess.run(
            ["goofys", "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("Goofys is already installed.")
    except subprocess.CalledProcessError:
        print(
            "ERROR: Goofys is not installed. Please install Goofys before using this script."
        )
        raise typer.Exit(1)


def ensure_directory_exists(directory: str):
    """Ensure a directory exists."""
    if not os.path.isdir(directory):
        print(f"Creating directory: {directory}")
        os.makedirs(directory, exist_ok=True)


def is_mount_point(mount_point: str) -> bool:
    """Check if a directory is a mount point."""
    return (
        subprocess.run(["mountpoint", "-q", mount_point], check=False).returncode == 0
    )


@cloud_app.command(help="Add a new AWS profile to ~/.aws/config.")
def s3_config(
    profile_name: str = typer.Argument(..., help="AWS profile name to add."),
    region: str = typer.Argument(..., help="AWS region (e.g., us-west-2)."),
    aws_access_key_id: str = typer.Argument(..., help="Your AWS access key ID."),
    aws_secret_access_key: str = typer.Argument(
        ..., help="Your AWS secret access key."
    ),
    endpoint_url: str = typer.Option(
        None, help="Optional custom AWS endpoint URL."
    ),  # New optional endpoint_url argument
):
    """
    Add a new AWS profile to ~/.aws/config.
    """
    aws_config_file = os.path.expanduser("~/.aws/config")
    aws_dir = os.path.dirname(aws_config_file)

    # Ensure the AWS config directory exists
    os.makedirs(aws_dir, exist_ok=True)

    # Check if the profile already exists in the config file
    if os.path.exists(aws_config_file):
        with open(aws_config_file, "r") as config_file:
            if f"[{profile_name}]" in config_file.read():
                raise ValueError(
                    f"Profile '{profile_name}' already exists in {aws_config_file}."
                )

    # Add the profile to the config file
    print(f"Adding profile '{profile_name}' to AWS config...")
    with open(aws_config_file, "a") as config_file:
        config_file.write(
            f"\n[{profile_name}]\n"
            f"region = {region}\n"
            f"aws_access_key_id = {aws_access_key_id}\n"
            f"aws_secret_access_key = {aws_secret_access_key}\n"
        )

        # Only add the endpoint_url if it's provided
        if endpoint_url:
            config_file.write(f"endpoint_url = {endpoint_url}\n")

    print(f"Profile '{profile_name}' successfully added to {aws_config_file}.")
