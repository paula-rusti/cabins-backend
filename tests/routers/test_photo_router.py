from tempfile import SpooledTemporaryFile
from unittest.mock import MagicMock

from routers.photo_router import photo_repository
from tests.routers.fixtures import test_client


def test_photo_add(test_client):
    # Setup
    mock_photo_repository = MagicMock()
    test_client.app.dependency_overrides[
        photo_repository
    ] = lambda: mock_photo_repository

    fh = SpooledTemporaryFile()
    fh.write("abcdefasd".encode())
    files = {"file": ("images.png", fh, "image/png")}

    # Test
    response = test_client.post("/photos/1/add", files=files)

    # Assert
    response_content = response.json()
    assert response.status_code == 200
    assert response_content["filename"] == "images.png"
    assert response_content["cabin_id"] == "1"
    assert mock_photo_repository.add.called is True


def test_get_photo(test_client):
    # Setup
    mock_photo = MagicMock()
    mock_photo_repository = MagicMock()
    test_client.app.dependency_overrides[
        photo_repository
    ] = lambda: mock_photo_repository
    mock_photo_repository.get_by_id.return_value = mock_photo
    mock_photo.content = "poza fake"

    # Test
    response = test_client.get("/photos/1555")

    # Assert
    assert response.status_code == 200
    assert response.text == "poza fake"
    mock_photo_repository.get_by_id.assert_called_with(1555)
