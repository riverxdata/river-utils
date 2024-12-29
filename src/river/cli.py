import typer

from .setup.main import setup_app
from .cloud.main import cloud_app
from .job.main import job_app

__version__ = "1.0.4"



def version_callback(value: bool):
    if value:
        print(f"River CLI Version: {__version__}")
        raise typer.Exit()


# Initialize the Typer app
app = typer.Typer(
    add_completion=False,
    help="River CLI: A command-line tool for bioinformatics and HPC management",
)


# Add subcommands
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


@app.command()
def version():
    """
    Display the version of River CLI.
    """
    typer.echo(f"River CLI Version: {__version__}")


def main():
    app()


if __name__ == "__main__":
    main()
