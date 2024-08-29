from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from gh-test API"}

def test_hc_main():
    response = client.get("/hc")
    assert response.status_code == 200
    assert response.json() == {"message": "Health - OK"}
