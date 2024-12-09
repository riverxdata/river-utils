.PHONY: build test clean install slurm

# Variables
PYTHON := python3
BUILD_DIR := dist
VERSION := 1.0.0

dev:
	. env/bin/activate
	pip install -e .

test-install:
	RIVER_HOME="./tests/river_home_test_setup" pytest -k "setup" --cov=src --cov-report=term

test-base:
	RIVER_HOME="./tests/river_home" pytest --cov=src -k "not setup" --cov-report=term tests/

# Build the project
build:
	$(PYTHON) -m build

# Clean the build artifacts
clean:
	rm -rf $(BUILD_DIR) *.egg-info build

# Install the package locally
install:
	pip install --upgrade --force-reinstall $(BUILD_DIR)/*.whl

	