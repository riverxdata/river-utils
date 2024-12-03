#!/usr/bin/env python3
import os
import subprocess
import json
from pathlib import Path
import typer

app = typer.Typer()

BASEDIR = os.path.join(Path(__file__).parent, "templates")

# Paths to templates
DEFAULT_HEADER = os.path.join(BASEDIR, "default_header.template")
ACCESS_HEADER = os.path.join(BASEDIR, "access_header.template")
S3_TEMPLATE = os.path.join(BASEDIR, "s3.template")


def load_file(file_path):
    """Utility function to open and read a file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, "r") as f:
        return f.read()


class ScriptGenerator:
    _TEMPLATES = {
        "default_header": load_file(DEFAULT_HEADER),
        "access_header": load_file(ACCESS_HEADER),
        "s3_script": load_file(S3_TEMPLATE),
    }

    def __init__(
        self,
        git,
        version,
        config_file,
        tools_dir,
        job_script,
        bootstrap_script,
        output_file,
        allow_access,
    ):
        self.git = git
        self.version = version
        self.config_file = Path(config_file)
        self.tools_dir = Path(tools_dir)
        self.job_script = job_script
        self.bootstrap_script = bootstrap_script
        self.output_file = Path(output_file)
        self.allow_access = allow_access
        self._config_data = {}

    def _load_config(self):
        """Load and parse the configuration file."""
        if not self.config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_file}")
        try:
            with self.config_file.open("r") as file:
                self._config_data = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file: {e}")
        self._config_data["river_home"] = os.environ.get("RIVER_HOME", ".")
        self._config_data["analysis"] = self._get_tool_name()

    def _get_tool_name(self):
        """Extract the tool name from the Git repository URL."""
        return os.path.basename(self.git).rstrip(".git")

    def _clone_or_update_repo(self):
        """Clone the repository if it doesn't exist, or update it if it does."""
        local_repo = self.tools_dir / self._get_tool_name()
        if not local_repo.exists():
            try:
                subprocess.check_call(["git", "clone", self.git, str(local_repo)])
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"Failed to clone repository: {e}")
        else:
            try:
                subprocess.check_call(["git", "-C", str(local_repo), "fetch"])
                subprocess.check_call(
                    ["git", "-C", str(local_repo), "checkout", self.version]
                )
                subprocess.check_call(
                    ["git", "-C", str(local_repo), "pull", "origin", self.version]
                )
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"Failed to update repository: {e}")

    def _replace_placeholders(self, template):
        """Replace placeholders in the given template with configuration values."""
        for key, value in self._config_data.items():
            template = template.replace(f"<<{key}>>", str(value))
        return template

    def generate_script(self):
        """Generate the script based on the provided inputs."""
        tool_name = self._get_tool_name()
        job_script_path = self.tools_dir / tool_name / self.job_script
        bootstrap_script_path = (
            self.tools_dir / tool_name / self.bootstrap_script
            if self.bootstrap_script
            else None
        )

        # get repo
        self._clone_or_update_repo()
        if not job_script_path.exists():
            raise FileNotFoundError(f"Job script not found: {job_script_path}")

        # load config
        self._load_config()
        header = self._replace_placeholders(self._TEMPLATES["default_header"])
        access_header = (
            self._replace_placeholders(self._TEMPLATES["access_header"])
            if self.allow_access
            else ""
        )
        s3_script = self._replace_placeholders(self._TEMPLATES["s3_script"])

        bootstrap_content = ""
        if bootstrap_script_path and bootstrap_script_path.exists():
            with bootstrap_script_path.open("r") as file:
                bootstrap_content = self._replace_placeholders(file.read())

        with job_script_path.open("r") as file:
            job_content = self._replace_placeholders(file.read())

        script_content = f"{header}\n# Boostrap:\n{bootstrap_content}\n{access_header}\n{s3_script}\n{job_content}"
        with self.output_file.open("w") as file:
            file.write(script_content)
        os.chmod(self.output_file, 0o700)

        print(f"Generated script saved to {self.output_file}")


@app.command()
def create(
    git: str = typer.Option(
        ..., "--git", help="The Git repository URL to clone or fetch."
    ),
    version: str = typer.Option(
        ..., "--version", help="The version to checkout or tag."
    ),
    config_file: str = typer.Option(
        ..., "--config-file", help="Path to the JSON config file"
    ),
    tools_dir: str = typer.Option(..., "--tools-dir", help="Directory to store tools"),
    job_script: str = typer.Option(..., "--job-script", help="Path to the job script"),
    output_file: str = typer.Option(..., "--output-file", help="Output script file"),
    bootstrap_script: str = typer.Option(
        None, "--bootstrap-script", help="Optional bootstrap script"
    ),
    allow_access: bool = typer.Option(
        False, "--allow-access", help="Allow access via port"
    ),
):
    """Generate a job script based on the provided information."""
    script_generator = ScriptGenerator(
        git=git,
        version=version,
        config_file=config_file,
        tools_dir=tools_dir,
        job_script=job_script,
        bootstrap_script=bootstrap_script,
        output_file=output_file,
        allow_access=allow_access,
    )
    script_generator.generate_script()


if __name__ == "__main__":
    app()
