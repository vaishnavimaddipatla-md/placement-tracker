def test_signup_success(client):
    res = client.post(
        "/signup",
        json={"name": "Asha", "email": "asha@example.com", "password": "password123"},
    )
    assert res.status_code == 201
    body = res.json()
    assert body["email"] == "asha@example.com"
    assert "password" not in body
    assert "password_hash" not in body


def test_signup_duplicate_email(client):
    data = {"name": "Asha", "email": "asha@example.com", "password": "password123"}
    client.post("/signup", json=data)
    res = client.post("/signup", json=data)
    assert res.status_code == 400


def test_signup_short_password(client):
    res = client.post(
        "/signup",
        json={"name": "Asha", "email": "asha@example.com", "password": "short"},
    )
    assert res.status_code == 400


def test_login_success(client):
    client.post(
        "/signup",
        json={"name": "Asha", "email": "asha@example.com", "password": "password123"},
    )
    res = client.post("/login", json={"email": "asha@example.com", "password": "password123"})
    assert res.status_code == 200
    assert res.json()["access_token"]


def test_login_wrong_password(client):
    client.post(
        "/signup",
        json={"name": "Asha", "email": "asha@example.com", "password": "password123"},
    )
    res = client.post("/login", json={"email": "asha@example.com", "password": "wrongpass1"})
    assert res.status_code == 401


def test_me_requires_token(client):
    res = client.get("/me")
    assert res.status_code in (401, 403)


def test_me_returns_current_user(client, auth_headers):
    res = client.get("/me", headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["email"] == "test@example.com"