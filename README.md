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

First you need to setup postgres database

Then create .env file to configure database connection

Then run pytest
```commandline
uv run pytest
```

To run inside docker container:

```commandline
docker compose -f test-compose.yml up --build --exit-code-from run_pytest
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