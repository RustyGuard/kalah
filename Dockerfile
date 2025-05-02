FROM python:3.12.10-bookworm

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates
# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh
# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh
# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"
COPY ./pyproject.toml ./pyproject.toml
COPY ./uv.lock ./uv.lock
RUN uv sync

COPY ./src ./src
COPY ./migrations ./migrations
COPY ./static ./static
COPY ./templates ./templates
COPY ./tests ./tests
COPY ./asgi.py ./asgi.py
COPY ./.python-version ./.python-version
COPY ./.env ./.env

ENTRYPOINT uv run pytest
