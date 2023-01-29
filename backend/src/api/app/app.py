from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import DBAPIError, NoResultFound
from starlette.middleware.cors import CORSMiddleware

from api.config.database import get_sessionmaker
from api.config.settings import settings
from api.controller.http.router import api_router
from api.misc.exception_handlers import (
    db_exception_handler,
    db_not_found_handler,
    http_exception_handler,
)


def create_app() -> FastAPI:
    app = FastAPI(
        debug=settings.DEBUG,
        title=settings.TITLE,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        root_path=settings.ROOT_PATH,
    )

    app.add_middleware(CORSMiddleware, **settings.CORS_OPTIONS)

    @app.on_event("startup")
    async def db_state_session():
        app.state.db_session = get_sessionmaker()

    app.include_router(api_router, prefix=settings.API_PREFIX)

    app.add_exception_handler(DBAPIError, db_exception_handler)
    app.add_exception_handler(NoResultFound, db_not_found_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)

    return app
