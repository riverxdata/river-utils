#!/usr/bin/env python3
import subprocess
import json
import os
from pathlib import Path
import typer
from dotenv import load_dotenv

create_app = typer.Typer()

JOB_TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "job.template"


def load_file(file_path: Path) -> str:
    """Utility function to open and read a file."""
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    return file_path.read_text()


def load_config(config_file: Path) -> dict:
    """Load and parse the configuration file."""
    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_file}")
    try:
        config_data = json.loads(config_file.read_text())
        river_home = os.environ.get("RIVER_HOME", ".")
        # If river_home does not start with "/", use it as a relative path.
        config_data["river_home"] = (
            Path(river_home).resolve().as_posix()
            if river_home.startswith("/")
            else river_home
        )
        return config_data
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in config file: {e}")


def get_tool_name(git: str) -> str:
    """Extract the tool name from the Git repository URL."""
    return Path(git).stem


def clone_with_tag_only(git: str, tool_dir: Path, tag: str):
    """
    Clone a Git repository with the specified tag only.

    :param git: The Git repository URL.
    :param tag: The tag to checkout.
    :param tool_dir: Directory where the repository will be cloned.
    """
    # Derive tool name from the Git URL and prepare the local path
    tool_name = get_tool_name(git)
    local_repo = tool_dir / tool_name

    try:
        if not local_repo.exists():
            # Clone directly with the specified tag
            print(f"Cloning repository {git} with tag '{tag}' into {local_repo}...")
            subprocess.check_call(
                [
                    "git",
                    "clone",
                    "--branch",
                    tag,
                    "--single-branch",
                    git,
                    str(local_repo),
                ]
            )
        else:
            print(f"Repository {local_repo} already exists. Skipping clone.")
            # Optional: Verify if the correct tag is checked out
            current_tag = subprocess.check_output(
                ["git", "-C", str(local_repo), "describe", "--tags"], text=True
            ).strip()
            if current_tag != tag:
                raise RuntimeError(
                    f"Tag mismatch: expected '{tag}', but found '{current_tag}'."
                )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Git operation failed: {e}")


def replace_placeholders(template: str, config_data: dict) -> str:
    """Replace placeholders in the template with configuration values."""
    for key, value in config_data.items():
        template = template.replace(f"<<{key}>>", str(value))
    return template


def generate_script(git: str, version: str, job_id: str):
    """Generate a script based on the provided inputs."""
    RIVER_HOME = os.environ.get("RIVER_HOME", ".")
    if not RIVER_HOME:
        raise RuntimeError("RIVER_HOME environment variable is not set")
    # Adjust path based on whether it's relative or absolute
    RIVER_HOME = (
        Path(RIVER_HOME) if RIVER_HOME.startswith("/") else Path(".") / RIVER_HOME
    )
    TOOL_DIR = RIVER_HOME / ".river" / "tools"
    JOB_DIR = RIVER_HOME / ".river" / "jobs"
    output_file = JOB_DIR / job_id / "job.sh"
    config_file = JOB_DIR / job_id / "config.json"
    tool_name = get_tool_name(git)

    # Clone or update repository
    clone_with_tag_only(git, TOOL_DIR, version)

    # Load configuration
    config_data = load_config(config_file)

    # Prepare job script
    env_path = TOOL_DIR / tool_name / "river" / "env.sh"

    if env_path and load_dotenv(env_path) and os.environ.get("ALLOW_ACCESS") == "true":
        render_access = replace_placeholders(
            (
                'echo $(python3 -c "import socket; '
                "s=socket.socket(); "
                "s.bind(('', 0)); "
                "print(s.getsockname()[1]); "
                's.close()") > <<river_home>>/.river/jobs/<<uuid_job_id>>/job.port\n'
                "echo $(hostname) > <<river_home>>/.river/jobs/<<uuid_job_id>>/job.host\n"
            ),
            config_data,
        )
        config_data["access"] = render_access
    else:
        config_data["access"] = "# Tool does not have set the access"

    bootstrap_script_path = TOOL_DIR / tool_name / "river" / "bootstrap.sh"
    if bootstrap_script_path.exists():
        config_data["bootstrap"] = load_file(bootstrap_script_path)
    else:
        config_data["bootstrap"] = "# No bootstrap script\n"

    main_script_path = TOOL_DIR / tool_name / "river" / "main.sh"
    if not main_script_path.exists():
        raise FileNotFoundError(f"Job script not found: {main_script_path}")
    config_data["script"] = load_file(main_script_path)

    # Render
    template = load_file(JOB_TEMPLATE_PATH)
    filled_template = replace_placeholders(template, config_data)

    # Write output script
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(filled_template)
    output_file.chmod(0o700)
    typer.echo(f"Generated script saved to {output_file}")
