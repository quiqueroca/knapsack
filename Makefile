
test:
	PYTHONPATH=. uv run pytest tests/TestSacks.py

run:
	PYTHONPATH=. uv run python main.py

update-readme:
	PYTHONPATH=. uv run python update-leadboard.py


