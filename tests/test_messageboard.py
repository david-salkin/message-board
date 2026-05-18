import pytest
from httpx import AsyncClient
from uuid import uuid4

# Mark every test in that file with @pytest.mark.asyncio which allows us to use await
pytestmark = pytest.mark.asyncio


async def test_register_and_login(client: AsyncClient):
	# Test Registration
	username = f"tstuser_{uuid4().hex[:8]}"
	password = "qwerty123"
	reg_payload = {"username": username, "password": password}
	response = await client.post("/register", json=reg_payload)
	assert response.status_code == 201
	
	# Test Login
	login_data = {"username": username, "password": password}
	login_response = await client.post("/login", data=login_data)
	assert login_response.status_code == 200
	assert "access_token" in login_response.json()
	
	return login_response.json()["access_token"]


async def test_create_and_get_messages(client: AsyncClient):
	# Login to get token
	token = await test_register_and_login(client)
	headers = {"Authorization": f"Bearer {token}"}
	
	# Create Message
	msg_payload = {"content": "This board is going south!"}
	response = await client.post("/messages", json=msg_payload, headers=headers)
	assert response.status_code == 201

	msg_id = response.json()["id"]
	get_all = await client.get("/messages")
	assert get_all.status_code == 200

	messages = get_all.json()
	assert any(m["id"] == msg_id for m in messages)  # test that API returned the same message

	matching = next(m for m in messages if m["id"] == msg_id)  # retrieve message
	assert "upvotes" in matching  # requirement that votes are returned in response
	assert isinstance(matching["upvotes"], int)


async def test_voting_logic(client: AsyncClient):
	token = await test_register_and_login(client)
	headers = {"Authorization": f"Bearer {token}"}
	
	# Create a message to vote on
	msg = await client.post("/messages", json={"content": "Shameful and pathetic behaviour!"}, headers=headers)
	msg_id = msg.json()["id"]
	
	vote_payload = {"is_upvote": True}
	vote_res = await client.post(f"/messages/{msg_id}/vote", json=vote_payload, headers=headers)
	assert vote_res.status_code == 200


async def test_user_messages_excludes_vote_count(client: AsyncClient):
	token = await test_register_and_login(client)
	headers = {"Authorization": f"Bearer {token}"}

	# Create a message owned by the current user
	msg = await client.post("/messages", json={"content": "RIP my favorite violinist"}, headers=headers)
	assert msg.status_code == 201
	msg_id = msg.json()["id"]

	# Retrieve messages for the current user
	user_messages = await client.get("/user/messages", headers=headers)
	assert user_messages.status_code == 200
	messages = user_messages.json()
	assert any(m["id"] == msg_id for m in messages)

	matching = next(m for m in messages if m["id"] == msg_id)
	assert "upvotes" not in matching  # not votes in user messages response


async def test_multiple_vote_count(client: AsyncClient):
	token = await test_register_and_login(client)
	headers = {"Authorization": f"Bearer {token}"}

	msg = await client.post("/messages", json={"content": "Yay, another troll"}, headers=headers)
	assert msg.status_code == 201
	msg_id = msg.json()["id"]

	# Apply multiple votes to the same message
	votes = [True, True, False, True]
	for is_upvote in votes:
		resp = await client.post(f"/messages/{msg_id}/vote", json={"is_upvote": is_upvote}, headers=headers)
		assert resp.status_code == 200

	# Verify the final vote tally via the public messages endpoint
	all_messages = await client.get("/messages")
	assert all_messages.status_code == 200

	found = next((m for m in all_messages.json() if m["id"] == msg_id), None)
	assert found is not None
	assert found["upvotes"] == 2
