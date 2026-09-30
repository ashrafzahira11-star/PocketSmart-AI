import os

os.environ["USE_GEMINI"] = "false"
os.environ["SECRET_KEY"] = "test-secret"


from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home_page():

    response = client.get("/")

    assert response.status_code == 200

    assert "PocketSmart" in response.text


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json()["status"] == "ok"


def test_register_login_and_home_planner():

    username = "testuser_pocketsmart"

    password = "password123"


    register = client.post(

        "/register",

        data={
            "username": username,
            "password": password
        },

        follow_redirects=False,
    )


    assert register.status_code == 303


    login = client.post(

        "/login",

        data={
            "username": username,
            "password": password
        },

        follow_redirects=False,
    )


    assert login.status_code == 303


    response = client.post(

        "/api/generate-home",

        json={

            "budget": 50000,

            "rooms": [
                "Living Room",
                "Bedroom"
            ],

            "style": "Modern",

            "priorities": "storage",
        },
    )


    assert response.status_code == 200


    data = response.json()


    assert data["planner"] == "home"

    assert data["budget"] == 50000

    assert len(
        data["recommendations"]
    ) > 0