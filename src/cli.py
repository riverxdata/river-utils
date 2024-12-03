import typer
from .script.create import app as script_generator_app
from .job.monitor_state import app as job_monitor_state_app
from .setup.setup import app as setup_app
from .cloud.s3 import app as s3_cloud_app

app = typer.Typer()
app.add_typer(
    script_generator_app,
    name="script",
    help="Script utilities for SLURM",
)
app.add_typer(
    job_monitor_state_app,
    name="job",
    help="Cmd for job in slurm mangement",
)
app.add_typer(
    setup_app,
    name="setup",
    help="Set up utilities for bioinformatics analysis",
)
app.add_typer(
    s3_cloud_app,
    name="cloud",
    help="Set up s3",
)


def main():
    app()


if __name__ == "__main__":
    main()
