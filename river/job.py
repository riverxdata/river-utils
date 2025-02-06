from typing import List
import typer
import os

from river.utils.job_state import get_jobs_info
from river.utils.job_create import generate_script
from river.utils.job_nf_core import json_to_nextflow_config
from river.objects import Job
from river.const import RIVER_HOME
from river.logger import logger

job_app = typer.Typer()


@job_app.command()
def create(
    job_id: str = typer.Option(
        ..., "--job-id", help="The uuid job id retrieve information from RIVER_HOME"
    ),
):
    """Generate a job script based on the provided information."""
    generate_script(
        job_id=job_id,
    )


@job_app.command()
def config(
    job_id: str = typer.Option(
        ...,
        "--job-id",
        help="It will look for the config.json on the job folder in RIVER_HOME, generate river.config",
    ),
):
    """Generate a job script based on the provided information."""
    job_dir = os.path.join(RIVER_HOME, ".river", "jobs", job_id)
    config_json = os.path.join(job_dir, "config.json")
    river_config = os.path.join(job_dir, "river.config")
    if os.path.exists(river_config):
        logger.info(f"river.config is already generated at {river_config}")
    if not os.path.exists(config_json):
        logger.error(f"Not found config file at {job_dir}")

    json_to_nextflow_config(config_json, river_config)


@job_app.command()
def info(uuid_job_ids: List[str]):
    """Fetch and display information about jobs."""
    jobs = [Job(uuid_job_id=uuid) for uuid in uuid_job_ids]
    get_jobs_info(jobs)
    for job in jobs:
        typer.echo(job.to_dict())
