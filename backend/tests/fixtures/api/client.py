import logging

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from api.app.app import create_app


@pytest.fixture
def logger() -> logging.Logger:
    return logging.getLogger()


@pytest.fixture
async def app(patch_settings) -> FastAPI:
    return create_app()


@pytest.fixture
async def initialized_app(app: FastAPI, session_maker_fx, logger) -> FastAPI:
    app.state.db_session = session_maker_fx
    return app


@pytest.fixture
async def client(initialized_app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=initialized_app,
        base_url="http://testserver",
    ) as client:
        yield client
