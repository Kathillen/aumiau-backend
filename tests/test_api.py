from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_rota_inicial():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "API Aumiau funcionando!"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_documentacao():
    response = client.get("/openapi.json")

    assert response.status_code == 200
