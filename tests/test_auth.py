def test_register_user(client):
    response = client.post(
        "/register",
        json={"username": "alice", "password": "secret"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "User created"