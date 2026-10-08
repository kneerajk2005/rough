import pytest
from app import app, init_db, get_db_connection


@pytest.fixture
def client():
    app.config["TESTING"] = True

    # Make sure the database and users table exist
    init_db()

    with app.test_client() as client:
        yield client


def test_login_page(client):
    response = client.get("/login")

    assert response.status_code == 200


def test_register_page(client):
    response = client.get("/register")

    assert response.status_code == 200


def test_home_without_login(client):
    response = client.get("/")

    assert response.status_code == 302
    assert "/login" in response.location


def test_register_user(client):
    username = "jenkins_test_user"
    password = "test123"

    response = client.post(
        "/register",
        data={
            "username": username,
            "password": password
        },
        follow_redirects=False
    )

    assert response.status_code == 302
    assert response.location.endswith("/login")

    # Verify that the user was actually inserted into SQLite
    conn = get_db_connection()
    user = conn.execute(
        "SELECT username FROM users WHERE username = ?",
        (username,)
    ).fetchone()
    conn.close()

    assert user is not None
    assert user["username"] == username

    # Cleanup test user
    conn = get_db_connection()
    conn.execute(
        "DELETE FROM users WHERE username = ?",
        (username,)
    )
    conn.commit()
    conn.close()


def test_valid_login(client):
    username = "jenkins_login_test"
    password = "password123"

    # Create test user
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password)
    )
    conn.commit()
    conn.close()

    response = client.post(
        "/login",
        data={
            "username": username,
            "password": password
        },
        follow_redirects=False
    )

    assert response.status_code == 302
    assert response.location.endswith("/")

    # Cleanup
    conn = get_db_connection()
    conn.execute(
        "DELETE FROM users WHERE username = ?",
        (username,)
    )
    conn.commit()
    conn.close()


def test_invalid_login(client):
    response = client.post(
        "/login",
        data={
            "username": "wrong_user",
            "password": "wrong_password"
        }
    )

    assert response.status_code == 200
    assert b"Invalid username or password." in response.data