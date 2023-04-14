import pytest
from fastapi.testclient import TestClient

from main import create_app


@pytest.fixture
def test_client():
    client = TestClient(create_app())
    return client
