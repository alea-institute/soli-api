FROM ubuntu:24.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    pipx \
    curl \
    build-essential \
    &&  \
    rm -rf /var/lib/apt/lists/* \
    && \
    pipx install poetry \
    && \
    pipx ensurepath

# create /app directory
WORKDIR /app
RUN cd /app

# create /app directory
WORKDIR /app
RUN cd /app

# copy the poetry configuration \
COPY pyproject.toml poetry.lock ./

# build the poetry environment
RUN bash -l -c "poetry install --no-root"

# copy the python api code
COPY soli_api soli_api

# you could copy the config.json file, but we're using bind mounts by default instead.
# COPY config.json config.json

# run uvicorn: # uvicorn soli_api.api:app --reload
CMD ["bash", "-l", "-c", "PYTHONPATH=. poetry run uvicorn soli_api.api:app --host 0.0.0.0 --port 8000"]
EXPOSE 8000
