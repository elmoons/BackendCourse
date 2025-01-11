import pytest


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("nagibator2011@gmail.com", "qwerty123", 200),
        ("nagibator2011@gmail.com", "qwerty123", 409),
        ("nagibator2012@gmail.com", "cool1337", 200),
        ("abcde", "123", 422),
        ("abcde@abc", "123", 422),
    ],
)
async def test_auth_flow(email: str, password: str, status_code: int, ac):
    # /register
    response_reg = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )
    assert response_reg.status_code == status_code
    if status_code != 200:
        return

    # /login
    response_login = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert response_login.status_code == status_code
    assert ac.cookies["access_token"]
    assert "access_token" in response_login.json()

    # /me
    response_get_me = await ac.get("/auth/me")
    assert response_get_me.status_code == status_code
    user_data = response_get_me.json()
    assert user_data["email"] == email
    assert "id" in user_data
    assert "password" not in user_data
    assert "hashed_password" not in user_data

    # /logout
    response_logout = await ac.post("/auth/logout")
    assert response_logout.status_code == status_code
    assert "access_token" not in ac.cookies

    response_get_me = await ac.get("/auth/me")
    assert response_get_me.status_code == 401
