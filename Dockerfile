FROM python:3.10-slim

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.0.0

COPY backend /app/backend
COPY poetry.lock pyproject.toml entrypoint.sh /app/

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

ENTRYPOINT ["bash", "entrypoint.sh"]