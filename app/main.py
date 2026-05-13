from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from app.db.database import init_db
from app.middleware.logging import logging_middleware
from app.core.logging import configure_logging
from app.core.cfg import cfg_settings
import logging
from contextlib import asynccontextmanager
from app.api.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db() 
    yield  # DB is serving


configure_logging()
log = logging.getLogger(__name__)
log.info(f"{cfg_settings.app_name} has started.")

app = FastAPI(title=cfg_settings.app_name, lifespan=lifespan)

# Middleware
app.middleware("http")(logging_middleware)  # pass decorator, wraps all requests
app.add_middleware(GZipMiddleware, minimum_size=1000)  # pass class
app.include_router(router=router)


@app.get("/")
async def root():
    return {"message": "Message Board API running"}


@app.get("/health")
async def health():
    return {"ok": True}


