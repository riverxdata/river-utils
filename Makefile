.PHONY: dist test clean install slurm

# Variables
PYTHON := python3
BUILD_DIR := dist

dev:
	. env/bin/activate
	pip install -e .

unittest:
	RIVER_HOME="./tests/river_home" pytest tests --cov=src -k "not setup" --cov-report=term

# Build the project
$(BUILD_DIR):
	$(PYTHON) -m build

# Clean the build artifacts
clean:
	rm -rf $(BUILD_DIR) *.egg-info build

# Install the package locally
install:
	pip install --upgrade --force-reinstall $(BUILD_DIR)/*.whl

	