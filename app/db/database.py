from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool
from typing import AsyncGenerator
from sqlmodel import SQLModel
from app.core.cfg import cfg_settings


is_memory_db = ":memory:" in cfg_settings.DATABASE_URL  # are we working in the test environment?

# StaticPool causes the in-memory SQLite connection persistent across sessions because
# normally :memory: evaoprates the state - it creates a separate db for each connection
engine = create_async_engine(
	cfg_settings.DATABASE_URL,
	echo=cfg_settings.sql_debug,
	poolclass=StaticPool if is_memory_db else None,
	connect_args={"check_same_thread": False} if is_memory_db else {}
)
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
