from typing import List
import typer

from .utils.state import get_jobs_info
from .utils.create import generate_script
from .objs.job import Job


job_app = typer.Typer()


@job_app.command()
def create(
    git: str = typer.Option(
        ..., "--git", help="The Git repository URL to clone or fetch."
    ),
    version: str = typer.Option(
        ..., "--version", help="The version to checkout or tag."
    ),
    job_id: str = typer.Option(
        ..., "--job-id", help="The uuid job id retrieve information from RIVER_HOME"
    ),
):
    """Generate a job script based on the provided information."""
    generate_script(
        git=git,
        version=version,
        job_id=job_id,
    )


@job_app.command()
def info(uuid_job_ids: List[str]):
    """Fetch and display information about jobs."""
    jobs = [Job(uuid_job_id=uuid) for uuid in uuid_job_ids]
    get_jobs_info(jobs)
    for job in jobs:
        typer.echo(job.to_dict())
