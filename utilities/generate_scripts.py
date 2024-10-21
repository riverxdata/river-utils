#!/usr/bin/env python3
import os
import subprocess
import json
import argparse
from pathlib import Path

DEFAULT_HEADER = """#!/bin/bash
#SBATCH --job-name=<<uuid_job_id>>
#SBATCH --time=<<times>>
#SBATCH --output=<<river_home>>/.river/jobs/<<uuid_job_id>>/job.log
#SBATCH --mem=<<memory>>
#SBATCH --cpus-per-task=<<cpus>>
set -e
source ~/.river.sh
"""
ACCESS_HEADER = """
PORT=$(python3 -c 'import socket; s=socket.socket(); s.bind(("", 0)); print(s.getsockname()[1]); s.close()')
echo $(hostname) > "<<river_home>>/.river/jobs/<<uuid_job_id>>/job.host"
echo $PORT > "<<river_home>>/.river/jobs/<<uuid_job_id>>/job.port"
PASSWORD=$(openssl rand -base64 20)
echo $PASSWORD > "<<river_home>>/.river/jobs/<<uuid_job_id>>/job.password"
"""
MOUNT_S3_SCRIPT = """
s3_cloud.sh <<project_name>> <<endpoint>> <<river_home>>/.river/jobs/<<uuid_job_id>>/workspace <<bucket_name>>
"""
UMOUNT_S3_SCRIPT = """
s3_umount.sh <<river_home>>/.river/jobs/<<uuid_job_id>>/workspace
"""


def get_tool_name_path(
    tools_dir: str,
    git: str,
    job_script: str,
):
    """Get the tool name and job script path
    Args:
        tool_dir (str): Directory to store the tools
        git (str): Git repository URL
        job_script (str): Job script to execute
    """
    tool_name = os.path.basename(git).rstrip(".git")
    local_repo = os.path.join(tools_dir, tool_name)
    job_script_path = Path(os.path.join(tools_dir, tool_name, job_script))
    return tool_name, local_repo, job_script_path


def clone_or_update_repo(
    git,
    local_repo,
    version,
):
    if not os.path.exists(os.path.expanduser(local_repo)):
        try:
            subprocess.check_call(f"git clone {git} {local_repo}", shell=True)
        except subprocess.CalledProcessError:
            raise Exception("Failed to clone the repository")
    else:
        try:
            subprocess.check_call(
                f"cd {local_repo} && git fetch && git checkout {version} && git pull origin {version}",
                shell=True,
            )
        except subprocess.CalledProcessError:
            raise Exception("Failed to update the repository")


def load_json_file(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def replace_placeholders(template, replacements):
    for key, value in replacements.items():
        placeholder = f"<<{key}>>"
        template = template.replace(placeholder, str(value))
    return template


def generate_script(
    git,
    version,
    allow_access,
    config_file,
    tools_dir,
    job_script,
    output_file,
):
    tool_name, local_repo, job_script_path = get_tool_name_path(
        tools_dir,
        git,
        job_script,
    )
    clone_or_update_repo(git, local_repo, version)
    config_data = load_json_file(config_file)
    config_data["river_home"] = os.environ.get("RIVER_HOME", ".")
    # generate script
    header = replace_placeholders(DEFAULT_HEADER, config_data)
    access_header = replace_placeholders(ACCESS_HEADER, config_data)
    mount_s3 = replace_placeholders(MOUNT_S3_SCRIPT, config_data)
    with open(os.path.expanduser(job_script_path), "r") as file:
        main_script = file.read()
        main_script = replace_placeholders(main_script, config_data)
    umount_s3 = replace_placeholders(UMOUNT_S3_SCRIPT, config_data)

    # write script
    with open(os.path.expanduser(output_file), "w") as file:
        file.write(header)
        # write allow access to export via port
        if allow_access:
            file.write("\n" + access_header)
        # write before script to mount s3 for all jobs
        # file.write("\n" + mount_s3)
        file.write("\n" + main_script)
        # file.write("\n" + umount_s3)

    os.chmod(output_file, 0o700)
    print(f"Generated script with parameters has been saved to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate script with parameters")
    parser.add_argument("-git", required=True, help="Git repository URL")
    parser.add_argument(
        "-version", required=True, help="Version to checkout from the repository"
    )
    parser.add_argument(
        "-config_file",
        required=True,
        help="Path to the JSON file containing configuration",
    )
    parser.add_argument(
        "-tools_dir", required=True, help="Directory to store the tools"
    )
    parser.add_argument("-job_script", required=True, help="Job script to execute")
    parser.add_argument("-output_file", required=True, help="Output script file")
    parser.add_argument(
        "--allow_access", action="store_true", help="Allow access to outside scripts"
    )
    args = parser.parse_args()

    generate_script(
        args.git,
        args.version,
        args.allow_access,
        args.config_file,
        args.tools_dir,
        args.job_script,
        args.output_file,
    )
