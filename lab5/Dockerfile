FROM python:3.13-slim-bookworm
LABEL authors="e1_m"

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    build-essential \
    g++ && \
    rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

COPY pyproject.toml ./
RUN uv sync --no-dev

COPY rules_service rules_service

EXPOSE 8000

WORKDIR rules_service

CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]