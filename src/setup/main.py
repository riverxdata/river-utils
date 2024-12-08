import os
import subprocess
import typer
import shutil


setup_app = typer.Typer()

# Default versions for tools
openvscode_server_version = "1.93.1"
goofys_version = "0.24.0"


# Function to run shell commands safely
def run_command(command: str):
    """Run a shell command and raise an error if it fails."""
    result = subprocess.run(command, shell=True, check=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Command failed: {command}")


@setup_app.command()
def install(
    river_home: str = typer.Option(
        os.getenv("RIVER_HOME", os.path.expanduser("~")),
        help="The path to the RIVER_HOME directory.",
    )
):
    """Setup River utilities."""

    # Check if River utilities are already installed
    if os.path.isfile(f"{river_home}/.river.sh"):
        print("River utilities already installed.")
        print(
            f"To reinstall, remove the folder '{river_home}/.river' and run the script again."
        )
        raise typer.Exit()

    river_home_tools = f"{river_home}/.river/tools"

    # Create tools directory
    os.makedirs(river_home_tools, exist_ok=True)
    print("Start to install ...")
    # Install openvscode-server
    print(f"Installing openvscode-server v{openvscode_server_version}...")
    openvscode_url = f"https://github.com/gitpod-io/openvscode-server/releases/download/openvscode-server-v{openvscode_server_version}/openvscode-server-v{openvscode_server_version}-linux-x64.tar.gz"
    run_command(
        f"wget {openvscode_url} -O {river_home_tools}/openvscode-server-v{openvscode_server_version}-linux-x64.tar.gz"
    )
    run_command(
        f"tar -xzf {river_home_tools}/openvscode-server-v{openvscode_server_version}-linux-x64.tar.gz -C {river_home_tools}"
    )
    os.remove(
        f"{river_home_tools}/openvscode-server-v{openvscode_server_version}-linux-x64.tar.gz"
    )

    # Install goofys
    print(f"Installing goofys v{goofys_version}...")
    goofys_url = (
        f"https://github.com/kahing/goofys/releases/download/v{goofys_version}/goofys"
    )
    run_command(f"wget {goofys_url} -O {river_home_tools}/goofys")
    run_command(f"chmod u+x {river_home_tools}/goofys")

    # Install micromamba
    print("Installing micromamba...")
    micromamba_url = "https://micro.mamba.pm/api/micromamba/linux-64/latest"
    run_command(
        f"curl -Ls {micromamba_url} | tar -xvj -C {river_home_tools} bin/micromamba"
    )

    # Rename micromamba binary to correct location
    os.rename(
        f"{river_home_tools}/bin/micromamba",
        f"{river_home_tools}/micromamba2",
    )
    os.rename(
        f"{river_home_tools}/micromamba2",
        f"{river_home_tools}/micromamba",
    )

    # Install singularity and nextflow using micromamba
    print("Installing Singularity and Nextflow...")
    run_command(
        f"export MAMBA_ROOT_PREFIX={river_home}/.river/images/micromamba && {river_home_tools}/micromamba create -n river conda-forge::singularity bioconda::nextflow -y"
    )

    # Create .river.sh for environment variables
    RIVER_BIN = os.path.dirname(
        subprocess.check_output("which river", shell=True)
    ).decode("utf-8")
    print("Creating .river.sh to export river utilities' environment variables...")
    with open(f"{river_home}/.river.sh", "w") as f:
        f.write(
            f"""
export RIVER_HOME="{river_home}"
export RIVER_HOME_TOOLS=${{RIVER_HOME}}/.river/tools
export MAMBA_ROOT_PREFIX=${{RIVER_HOME}}/.river/.images/micromamba
export SINGULARITY_CACHE_DIR=${{RIVER_HOME}}/.river/.images/singularities
export NXF_SINGULARITY_CACHEDIR=$SINGULARITY_CACHE_DIR
export PATH=${{RIVER_HOME_TOOLS}}:${{RIVER_HOME_TOOLS}}/openvscode-server-v{openvscode_server_version}-linux-x64/bin:${RIVER_BIN}:$PATH
eval "$(micromamba shell hook -s posix)"
micromamba activate -n river
"""
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
    # Check if .river.sh exists to confirm installation
    if not os.path.isfile(f"{river_home}/.river.sh"):
        print("River utilities not installed.")
        raise typer.Exit()

    # Remove the tools directory and all its contents
    print(f"Cleaning up River utilities from {river_home}...")
    try:
        shutil.rmtree(f"{river_home}/.river")
        os.remove(f"{river_home}/.river.sh")
        print(f"Successfully cleaned up {river_home}/.river.")
    except Exception as e:
        print(f"Error cleaning up: {e}")
        raise typer.Exit()
