
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_get_on_post_status():
    response = client.get("/predict")
    assert response.status_code == 404