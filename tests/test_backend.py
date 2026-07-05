from pathlib import Path
import sys

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from backend.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_validate_endpoint_returns_processed_result(client):
    payload = {
        "raw_input": "Name : john doeEmail : john@gmailPhone : 9876543Age : twenty fiveBlood Group : ABCAddress : Hyderabad"
    }
    response = client.post("/validate", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["corrected_data"]["name"] == "John Doe"
    assert body["corrected_data"]["email"] == "john@gmail.com"
    assert body["corrected_data"]["phone"] is None
    assert body["corrected_data"]["age"] == 25
