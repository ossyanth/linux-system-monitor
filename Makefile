.PHONY: setup test run clean

setup:
	uv sync

test:
	uv run pytest

run:
	uv run python monitor.py

clean:
	rm -rf .venv