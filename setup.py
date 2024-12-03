from setuptools import setup

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
