from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
# StaticPool makes the in-memory SQLite connection persistent across sessions
# :memory: creates a separate database for each connection
from sqlalchemy.pool import StaticPool
from typing import AsyncGenerator
from sqlmodel import SQLModel
from app.core.cfg import cfg_settings


engine = create_async_engine(cfg_settings.DATABASE_URL, echo=cfg_settings.sql_debug, connect_args={"check_same_thread": False}, poolclass=StaticPool)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def init_db():
	async with engine.begin() as conn:
		await conn.run_sync(SQLModel.metadata.create_all)

"""
	Prerequisite for providing an async session to routes.
	Returns: not a session but a generator (declared in typing) which will produce a session
"""
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
	async with async_session_maker() as session:
		yield session
