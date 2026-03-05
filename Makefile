.PHONY: install run sync

install:
	uv sync

run:
	uv run python -m src.main

sync:
	uv sync
