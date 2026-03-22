import pytest
from blackjack.web.app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_index(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"BLACK JACK" in resp.data


def test_bet(client):
    client.get("/")  # init session
    resp = client.post("/bet", data={"amount": "10"})
    assert resp.status_code == 200
    assert b"Your Hand" in resp.data


def test_invalid_bet(client):
    client.get("/")
    resp = client.post("/bet", data={"amount": "0"})
    assert resp.status_code == 200
    assert b"Invalid bet" in resp.data


def test_hit(client):
    client.get("/")
    client.post("/bet", data={"amount": "10"})
    resp = client.post("/hit")
    assert resp.status_code == 200


def test_stand(client):
    client.get("/")
    client.post("/bet", data={"amount": "10"})
    resp = client.post("/stand")
    assert resp.status_code == 200
    # Should be round_over
    assert b"Deal Again" in resp.data or b"Game Over" in resp.data


def test_new_round(client):
    client.get("/")
    client.post("/bet", data={"amount": "10"})
    client.post("/stand")
    resp = client.post("/new-round")
    assert resp.status_code == 200
    assert b"Place your bet" in resp.data


def test_reset(client):
    client.get("/")
    resp = client.post("/reset")
    assert resp.status_code == 200
    assert b"Place your bet" in resp.data


def test_full_game_flow(client):
    """Play a complete round: bet -> stand -> new round."""
    client.get("/")
    client.post("/bet", data={"amount": "25"})
    client.post("/stand")
    resp = client.post("/new-round")
    assert resp.status_code == 200
