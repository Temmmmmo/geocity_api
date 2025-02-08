from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware

from backend import __version__
from backend.routes.city import city
from backend.settings import get_settings

settings = get_settings()
app = FastAPI(
    title="geocity_api",
    description="Краткое описание",
    version=__version__,
    docs_url=None if __version__ != "dev" else "/docs",
    redoc_url=None,
)


app.add_middleware(
    DBSessionMiddleware,
    db_url=str(settings.DB_DSN),
    engine_args={"pool_pre_ping": True, "isolation_level": "AUTOCOMMIT"},
)

app.include_router(city)
