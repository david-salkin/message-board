from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from typing import AsyncGenerator
from sqlmodel import SQLModel
from app.core.cfg import cfg_settings

DB_URL = "sqlite+aiosqlite:///./database.db"  # aiosqlite for async driver

engine = create_async_engine(DB_URL, echo=cfg_settings.sql_debug, connect_args={"check_same_thread": False})
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
