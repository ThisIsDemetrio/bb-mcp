sync:
	@uv sync

lint:
	@uv run ruff check .

format:
	@uv run ruff format .

start:
	@uv run --env-file .env bb-mcp
