import typer


from .setup.main import setup_app
from .cloud.main import cloud_app
from .job.main import job_app

app = typer.Typer()

app.add_typer(
    cloud_app,
    name="cloud",
    help="Set up s3 to use goofys to mount bucket on local storage",
)

app.add_typer(
    job_app,
    name="job",
    help="Job utilities for HPC management and river web server",
)
app.add_typer(
    setup_app,
    name="setup",
    help="Set up the standard tools for bioinformatics analysis",
)


def main():
    app()


if __name__ == "__main__":
    main()
