from tests.routers.fixtures import test_client


def test_get_docs(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
