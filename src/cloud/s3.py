import os
import subprocess
import typer

app = typer.Typer()


# S3 Config Command
@app.command()
def s3_config(profile: str, endpoint: str, mount_point: str, bucket: str):
    """
    Generate s3 profile in ~/.aws/config
    Args:
        profile (str): The profile name
        endpoint (str): The endpoint url
        mount_point (str): The mount point
        bucket (str): _description_

    Raises:
        typer.Exit: _description_
    """

    # Ensure the mount point directory exists
    if not os.path.isdir(mount_point):
        print(f"Creating mount point directory {mount_point}...")
        os.makedirs(mount_point, exist_ok=True)

    # Check if goofys is installed
    try:
        subprocess.run(
            ["goofys", "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("goofys is already installed.")
    except subprocess.CalledProcessError:
        print(
            "ERROR: goofys is not installed. Please install goofys before running this script."
        )
        raise typer.Exit(1)

    print(
        f"Configured S3 with profile {profile}, endpoint {endpoint}, bucket {bucket}, mounted at {mount_point}."
    )


# S3 Mount Command
@app.command()
def s3_mount(profile: str, endpoint: str, mount_point: str, bucket: str):
    """Mount an S3 bucket using Goofys."""

    # Ensure the mount point directory exists
    if not os.path.isdir(mount_point):
        print(f"Creating mount point directory {mount_point}...")
        os.makedirs(mount_point, exist_ok=True)

    # Check if goofys is installed
    try:
        subprocess.run(
            ["goofys", "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("goofys is already installed.")
    except subprocess.CalledProcessError:
        print(
            "ERROR: goofys is not installed. Please install goofys before running this script."
        )
        raise typer.Exit(1)

    # Check if the mount point is already mounted
    try:
        result = subprocess.run(["mountpoint", "-q", mount_point], check=True)
        if result.returncode == 0:
            print(f"{mount_point} is already mounted.")
        else:
            print(f"{mount_point} is not mounted. Mounting with goofys...")
            subprocess.run(
                [
                    "goofys",
                    "--profile",
                    profile,
                    "--file-mode=0700",
                    "--dir-mode=0700",
                    "--endpoint",
                    endpoint,
                    bucket,
                    mount_point,
                ],
                check=True,
            )
            print(f"Successfully mounted {bucket} to {mount_point}.")
    except subprocess.CalledProcessError:
        print(f"{mount_point} is not mounted. Mounting with goofys...")
        subprocess.run(
            [
                "goofys",
                "--profile",
                profile,
                "--file-mode=0700",
                "--dir-mode=0700",
                "--endpoint",
                endpoint,
                bucket,
                mount_point,
            ],
            check=True,
        )
        print(f"Successfully mounted {bucket} to {mount_point}.")


# S3 Umount Command
@app.command()
def s3_umount(mount_point: str):
    """Unmount an S3 bucket."""

    # Check if the mount point is currently mounted
    if subprocess.run(["mountpoint", "-q", mount_point], check=False).returncode == 0:
        print(f"{mount_point} is mounted. Unmounting...")
        subprocess.run(["umount", mount_point], check=True)
        print(f"{mount_point} has been successfully unmounted.")
    else:
        print(f"{mount_point} is not mounted.")


if __name__ == "__main__":
    app()
