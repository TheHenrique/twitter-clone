# `python-base` sets up all our shared environment variables
FROM python:3.12-slim as python-base

    # python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        build-essential

RUN pip install poetry

WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root

WORKDIR /app

COPY . /app/

RUN chmod +x start.sh

EXPOSE 8000

CMD ["./start.sh"]