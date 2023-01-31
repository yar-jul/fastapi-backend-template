FROM python:3.10-slim
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_NO_INTERACTION=1 \
    VIRTUAL_ENV=/opt/venv \
    PYTHONPATH='/app/src'
RUN apt-get update && apt-get install -y gcc libffi-dev g++ curl make
WORKDIR /app/
RUN curl -sSL https://install.python-poetry.org | python -
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:/root/.local/bin:$PATH"
COPY . .
RUN poetry install --without dev
RUN chmod -R +x scripts
ENTRYPOINT ["./scripts/entrypoint.sh"]
CMD ["./scripts/run.sh"]
