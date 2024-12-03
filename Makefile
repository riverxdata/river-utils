.PHONY: build test clean install

# Variables
PYTHON := python3
BUILD_DIR := dist

# Test the project
test:
	pytest -vvvv tests

# Build the project
build:
	$(PYTHON) -m build

# Clean the build artifacts
clean:
	rm -rf $(BUILD_DIR) *.egg-info build

# Install the package locally
install:
	pip install --upgrade --force-reinstall $(BUILD_DIR)/*.whl
