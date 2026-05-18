import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest_asyncio.fixture
async def client():
    """
    The test client must run FastAPI’s startup lifecycle, so that init_db() will
    execute and the user table will be created.
    """
    transport = ASGITransport(app=app)
    async with app.router.lifespan_context(app):
        async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
            yield ac
