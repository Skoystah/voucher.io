FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.8.5 /uv /uvx /bin/

# Copy the project into the image
ADD . /app

# Sync the project into a new environment, asserting the lockfile is up to date
WORKDIR /app
RUN uv sync --locked --no-dev

# Presuming there is a `my_app` command provided by the project
CMD ["uv", "run", "src/main.py"]
