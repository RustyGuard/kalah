# kalah

## Configuration

- Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Create `.venv` with ```uv sync``` command

## Start

```commandline
uv run fastapi dev src/main.py
```


## Code tools

### Code formatting and linting

```commandline
uv run ruff check --fix src
uv run ruff check --select I --fix src
uv run ruff format src
```

### Type checking

```commandline
uv run mypy src
```
