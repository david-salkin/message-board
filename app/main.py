from fastapi import FastAPI, Depends
from fastapi.middleware.gzip import GZipMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db import create_db
from app.middleware.logging import logging_middleware
from app.core.logging import configure_logging
from app.core.cfg import cfg_settings
import logging
#from models import Item

configure_logging()

log = logging.getLogger(__name__)

app = FastAPI(title=cfg_settings.app_name)
log.info(f"{cfg_settings.app_name=} {cfg_settings.SECRET_KEY=}")

app.middleware("http")(logging_middleware)  # wraps all requests
app.add_middleware(GZipMiddleware, minimum_size=1000)

create_db()

@app.get("/")
async def root():
    return {"message": "Message Board API running"}

@app.get("/health")
async def health():
    return {"ok": True}

