import typer
from .script.create import app as script_generator_app
from .job.monitor_state import app as job_monitor_state_app
from .setup.setup import app as setup_app

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


def main():
    app()


if __name__ == "__main__":
    main()
