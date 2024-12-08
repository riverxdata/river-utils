.PHONY: build test clean install slurm

# Variables
PYTHON := python3
BUILD_DIR := dist
VERSION := 1.0.0

dev:
	. env/bin/activate
	pip install -e .
# Test the project
test:
	RIVER_HOME="./tests/river_home" pytest --cov=src --cov-report=term tests/test_setup_install.py

slurm: ./dist/river-$(VERSION)-py3-none-any.whl
	cp ./dist/river-$(VERSION)-py3-none-any.whl slurm/river-$(VERSION)-py3-none-any.whl
	docker build slurm -t river-utils-slurm:$(VERSION)

slurm-start: ./dist/river-$(VERSION)-py3-none-any.whl slurm
	docker run --rm -d \
	-p 22:22 \
	-v ./dist:/home/river/dist \
	river-utils-slurm:$(VERSION)

# Build the project
build:
	$(PYTHON) -m build

# Clean the build artifacts
clean:
	rm -rf $(BUILD_DIR) *.egg-info build

# Install the package locally
install:
	pip install --upgrade --force-reinstall $(BUILD_DIR)/*.whl

	