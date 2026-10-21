run_tests:
	uv run pytest tests -v
	ruff check .
