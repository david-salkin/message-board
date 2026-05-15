import pytest
from httpx import AsyncClient
from app.main import app

# This allows us to use 'await' inside our test functions
pytestmark = pytest.mark.asyncio

async def test_register_and_login(client: AsyncClient):
    # 1. Test Registration
    reg_payload = {"username": "testuser", "password": "securepassword123"}
    response = await client.post("/register", json=reg_payload)
    assert response.status_code == 201
    
    # 2. Test Login (Form Data as per your router comment)
    login_data = {"username": "testuser", "password": "securepassword123"}
    login_response = await client.post("/login", data=login_data)
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
    return login_response.json()["access_token"]

async def test_create_and_get_messages(client: AsyncClient):
    # Login to get token
    token = await test_register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create Message
    msg_payload = {"content": "Hello Artisan World!"}
    response = await client.post("/messages", json=msg_payload, headers=headers)
    assert response.status_code == 201
    msg_id = response.json()["id"]
    
    # Get All Messages (Public)
    get_all = await client.get("/messages")
    assert get_all.status_code == 200
    assert any(m["id"] == msg_id for m in get_all.json())

async def test_voting_logic(client: AsyncClient):
    token = await test_register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create a message to vote on
    msg = await client.post("/messages", json={"content": "Vote for me"}, headers=headers)
    msg_id = msg.json()["id"]
    
    # Cast Upvote
    vote_payload = {"is_upvote": True}
    vote_res = await client.post(f"/messages/{msg_id}/vote", json=vote_payload, headers=headers)
    assert vote_res.status_code == 200
