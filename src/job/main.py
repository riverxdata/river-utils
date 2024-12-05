from typing import List
import typer

from .utils.state import get_jobs_info
from .objs.job import Job
from .objs.creator import Creator

job_app = typer.Typer()


@job_app.command()
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
    script_generator = Creator(
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


@job_app.command()
def info(uuid_job_ids: List[str]):
    """Fetch and display information about jobs."""
    jobs = [Job(uuid_job_id=uuid) for uuid in uuid_job_ids]
    get_jobs_info(jobs)
    for job in jobs:
        typer.echo(job.to_dict())


if __name__ == "__main__":
    job_app()
