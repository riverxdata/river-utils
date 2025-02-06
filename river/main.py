import typer
import importlib.metadata as importlib_metadata
from river.cloud import cloud_app
from river.job import job_app

# Initialize the Typer app
app = typer.Typer(
    add_completion=False,
    help="River CLI: A command-line tool for bioinformatics and HPC management",
)

# Sub commands
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


@app.command()
def version():
    """Print the version of the tool."""
    package_name = "river"
    typer.echo(importlib_metadata.version(package_name))


def main():
    app()


if __name__ == "__main__":
    main()
