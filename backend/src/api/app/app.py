from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.config.database import get_sessionmaker
from api.config.settings import settings


def create_app() -> FastAPI:
    app = FastAPI(
        debug=settings.DEBUG,
        title=settings.TITLE,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        root_path=settings.ROOT_PATH,
    )

    app.add_middleware(CORSMiddleware, **settings.CORS_OPTIONS)

    db_session_maker = get_sessionmaker()

    @app.on_event("startup")
    async def db_state_session():
        app.state.db_session = db_session_maker

    @app.on_event("shutdown")
    async def db_dispose_engine():
        await app.state.db_session.close_all()

    api_router = APIRouter()
    app.include_router(api_router, prefix=settings.API_PREFIX)

    return app
