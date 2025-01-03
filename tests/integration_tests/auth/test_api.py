import pytest


@pytest.mark.parametrize("email, password, status_code", [
    ("nagibator2011@gmail.com", "qwerty123", 200),
    ("nagibator2012@gmail.com", "cool1337", 200),
    ("nagibator2013@gmail.com", "qwerty123", 200),
])
async def test_authentication_and_authorization(
        email, password, status_code,
        ac):
    response_reg = await ac.post("/auth/register", json={
        "email": email,
        "password": password,
    })
    assert response_reg.status_code == status_code

    response_login = await ac.post("/auth/login", json={
        "email": email,
        "password": password,
    })
    assert response_login.status_code == status_code
    assert ac.cookies
    assert ac.cookies["access_token"]

    response_get_me = await ac.get("/auth/me")
    assert response_get_me.status_code == status_code
    user_data = response_get_me.json()
    assert user_data["id"]
    assert user_data["email"] == email

    response_logout = await ac.post("/auth/logout")
    assert response_logout.status_code == status_code
    assert not ac.cookies

