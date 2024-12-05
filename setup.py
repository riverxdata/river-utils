from setuptools import setup
from setuptools.command.install import install
import os
import subprocess


class PostInstallCommand(install):
    """Custom command to run setup.sh after the package is installed."""

    def run(self):
        install.run(self)
        setup_script_path = os.path.join(
            os.path.dirname(__file__), "src", "bin", "setup.sh"
        )
        if os.path.exists(setup_script_path):
            subprocess.check_call(["bash", setup_script_path])
        else:
            print(f"Warning: {setup_script_path} not found. Skipping setup script.")


setup(
    name="river",
    version="1.0.0",
    description="The cli tool for utilizing the data analysis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Thanh-Giang (River) Tan Nguyen",
    author_email="nttg8100@gmail.com",
    url="https://github.com/riverbioinformatics/code_server.git",
    license="MIT",
    packages=["src"],
    cmdclass={
        "install": PostInstallCommand,
    },
    package_dir={"src": "src"},
    include_package_data=True,
    install_requires=[
        "typer>=0.14.0",
    ],
    entry_points={
        "console_scripts": [
            "river=src.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
