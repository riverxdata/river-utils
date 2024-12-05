#!/usr/bin/env python3
import os
import subprocess
import json
from pathlib import Path
import typer

app = typer.Typer()


def load_file(file_path):
    """Utility function to open and read a file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, "r") as f:
        return f.read()


class Creator:
    JOB_TEMPLATE = os.path.join(
        os.path.join(Path(__file__).parent.parent, "templates"), "job.template"
    )

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
        self._template = load_file(self.JOB_TEMPLATE)

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

    def _get_script(self):
        """Replace placeholders in the given template with configuration values."""
        for key, value in self._config_data.items():
            self._template = self._template.replace(f"<<{key}>>", str(value))

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
        self._config_data["allow_access"] = (
            "echo $(hostname) > <<river_home>>/.river/jobs/<<uuid_job_id>>/job.host\n; "
        )
        self._config_data["boostrap"] = "# No boostrap script\n"
        if bootstrap_script_path and bootstrap_script_path.exists():
            with bootstrap_script_path.open("r") as file:
                self._config_data["boostrap"] = file.read()

        with job_script_path.open("r") as file:
            self._config_data["script"] = file.read()

        # write script
        self._get_script()
        with self.output_file.open("w") as file:
            file.write(self._template)
        os.chmod(self.output_file, 0o700)
        print(f"Generated script saved to {self.output_file}")
