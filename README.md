# kalah

## Configuration

- Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Create `.venv` with ```uv sync``` command

## Start

```commandline
uv run fastapi dev asgi.py
```


## Code tools

### Code formatting and linting

```commandline
uv run format.py
```

### Type checking

```commandline
uv run mypy src tests --explicit-package-bases
```


### Testing

```commandline
uv run pytest
```



### DB

#### Up
```commandline
uv run alembic upgrade head
```

#### Down
```commandline
uv run alembic downgrade -1
```

#### Create revision
```commandline
uv run alembic revision --autogenerate -m "message"
```