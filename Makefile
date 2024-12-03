.PHONY: build test

test:
	pytest -vvvv tests
	
build:
	python3 -m build 