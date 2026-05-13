from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db import create_db
from app.middleware.logging import logging_middleware
from app.core.logging import configure_logging
from app.core.cfg import cfg_settings
#from models import Item

configure_logging()

app = FastAPI(title=cfg_settings.app_name)
app.middleware("http")(logging_middleware)  # wraps all requests
create_db()

@app.get("/")
async def root():
    return {"message": "Message Board API running"}

@app.get("/health")
async def health():
    return {"ok": True}

