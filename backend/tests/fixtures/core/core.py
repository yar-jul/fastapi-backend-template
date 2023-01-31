from urllib.parse import urlparse, urlunparse

import pytest
from testcontainers.postgres import PostgresContainer

from api.app.app import get_sessionmaker
from migrations import migrations


@pytest.fixture(scope="session")
def db_container_url():
    postgis_container = PostgresContainer("postgres:14-alpine")
    with postgis_container as postgis:
        postgis_url = postgis.get_connection_url()
        async_postgis_url = urlunparse(urlparse(postgis_url)._replace(scheme="postgresql+asyncpg"))
        yield async_postgis_url


@pytest.fixture
def patch_settings(mocker, db_container_url):
    mocker.patch("api.config.settings.settings.SQLALCHEMY_DATABASE_DSN", db_container_url)
    yield


@pytest.fixture
def db_migrations(patch_settings):
    migrations.upgrade()
    yield db_container_url
    migrations.downgrade()


@pytest.fixture
async def session_maker_fx(db_migrations):
    return get_sessionmaker()
