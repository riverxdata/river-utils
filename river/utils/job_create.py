#!/usr/bin/env python3
import json
import os
from pathlib import Path
from river.logger import logger

# Define paths
JOB_TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "job.template"


def load_file(file_path: Path) -> str:
    """Utility function to open and read a file."""
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
    return file_path.read_text()


def load_config(config_file: Path) -> dict:
    """Load and parse the configuration file."""
    if not config_file.exists():
        logger.error(f"Configuration file not found: {config_file}")
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
        logger.error(f"Invalid JSON in config file: {e}")


def get_tool_name(git: str) -> str:
    """Extract the tool name from the Git repository URL."""
    return Path(git).stem


def replace_placeholders(template: str, config_data: dict) -> str:
    """Replace placeholders in the template with configuration values."""
    for key, value in config_data.items():
        template = template.replace(f"<<{key}>>", str(value))
    return template


def validate_config(config_data: dict):
    """Validate the configuration data."""
    required_fields = ["cpus", "memory", "times", "git", "tag", "uuid_job_id"]
    for field in required_fields:
        if field not in config_data:
            logger.error(f"Missing required field in config: {field}")


def generate_script(job_id: str):
    """Generate a script based on the provided inputs."""
    RIVER_HOME = os.environ.get("RIVER_HOME", ".")
    if not RIVER_HOME:
        logger.error("RIVER_HOME environment variable is not set")

    # Adjust path based on whether it's relative or absolute
    RIVER_HOME = (
        Path(RIVER_HOME).resolve()
        if RIVER_HOME.startswith("/")
        else Path(".") / RIVER_HOME
    )
    JOB_DIR = RIVER_HOME / ".river" / "jobs"
    output_file = JOB_DIR / job_id / "job.sh"
    config_file = JOB_DIR / job_id / "config.json"

    # Load and validate configuration
    config_data = load_config(config_file)
    validate_config(config_data)

    # Render template
    template = load_file(JOB_TEMPLATE_PATH)
    filled_template = replace_placeholders(template, config_data)

    # Write output script
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(filled_template)
    output_file.chmod(0o700)
    logger.info(f"Generated script saved to {output_file}")
