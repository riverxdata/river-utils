import os
import subprocess
import typer
import shutil

setup_app = typer.Typer()

# Default versions for tools
OPENVSCODE_SERVER_VERSION = "1.93.1"
GOOFYS_VERSION = "0.24.0"


def run_command(command: str):
    """Run a shell command and raise an error if it fails."""
    subprocess.run(command, shell=True, check=True, text=True)


@setup_app.command()
def install(
    river_home: str = typer.Option(
        os.getenv("RIVER_HOME", os.path.expanduser("~")),
        help="The path to the RIVER_HOME directory.",
    )
):
    """Setup River utilities."""
    tools_dir = os.path.join(river_home, ".river", "tools")
    bin_dir = os.path.join(river_home, ".river", "bin")

    os.makedirs(tools_dir, exist_ok=True)
    os.makedirs(bin_dir, exist_ok=True)
    print("Starting installation...")

    vscode_path = os.path.join(
        tools_dir,
        f"openvscode-server-v{OPENVSCODE_SERVER_VERSION}-linux-x64",
        "bin",
        "openvscode-server",
    )
    goofys_path = os.path.join(tools_dir, f"goofys/v{GOOFYS_VERSION}", "goofys")

    # openvscode-server
    if not os.path.exists(vscode_path):
        print(f"Installing openvscode-server v{OPENVSCODE_SERVER_VERSION}...")
        openvscode_url = (
            f"https://github.com/gitpod-io/openvscode-server/releases/download/"
            f"openvscode-server-v{OPENVSCODE_SERVER_VERSION}/openvscode-server-v{OPENVSCODE_SERVER_VERSION}-linux-x64.tar.gz"
        )
        tar_path = os.path.join(
            tools_dir,
            f"openvscode-server-v{OPENVSCODE_SERVER_VERSION}-linux-x64.tar.gz",
        )
        run_command(f"wget {openvscode_url} -O {tar_path}")
        run_command(f"tar -xzf {tar_path} -C {tools_dir}")
        os.remove(tar_path)

    run_command(
        f"ln -sf {vscode_path}  {os.path.join(bin_dir, 'openvscode-server')}",
    )

    # goofys
    if not os.path.exists(goofys_path):
        print(f"Installing goofys v{GOOFYS_VERSION}...")
        goofys_url = f"https://github.com/kahing/goofys/releases/download/v{GOOFYS_VERSION}/goofys"
        os.makedirs(os.path.dirname(goofys_path), exist_ok=True)
        run_command(f"wget {goofys_url} -O {goofys_path}")
        run_command(f"chmod u+x {goofys_path}")

    run_command(
        f"ln -sf {goofys_path}  {os.path.join(bin_dir, 'goofys')}",
    )
    print("Setup complete!")


@setup_app.command()
def clean(
    river_home: str = typer.Option(
        os.getenv("RIVER_HOME", os.path.expanduser("~")),
        help="The path to the RIVER_HOME directory.",
    )
):
    """Clean up all installed River utilities."""
    river_dir = os.path.join(river_home, ".river", "tools")

    if not os.path.exists(river_dir):
        print("River tools are not installed.")
        raise typer.Exit()

    print(f"Cleaning up River tools from {river_home}...")
    try:
        shutil.rmtree(river_dir)
        print(f"Successfully cleaned up {river_dir}.")
    except Exception as e:
        print(f"Error during cleanup: {e}")
        raise typer.Exit()


if __name__ == "__main__":
    setup_app()
