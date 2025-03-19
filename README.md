# kalah

## Configuration

- Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Create `.venv` with ```uv sync``` command

## Start

```commandline
uv run fastapi dev src/main.py
```


## Code tools

### Black

Code formatter

```commandline
uv run black
```

### Mypy

Type checker

```commandline
uv run mypy src
```

### Ruff

Linter

```commandline
uv run ruff check src
```