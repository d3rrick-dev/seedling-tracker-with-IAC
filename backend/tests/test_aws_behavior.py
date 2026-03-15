import pytest
from unittest.mock import MagicMock
from app.services.seedling_service import SeedlingService


def test_upload_photo_triggers_s3_and_sqs(mocker):
    mock_upload = mocker.patch("app.services.seedling_service.upload_to_s3")
    mock_notify = mocker.patch("app.services.seedling_service.notify_worker")
    
    mock_repo = MagicMock()
    mock_seedling = MagicMock(id=1, image_url=None)
    mock_repo.get_by_id.return_value = mock_seedling
    
    service = SeedlingService(db=MagicMock())
    service.repo = mock_repo
    
    mock_upload.return_value = "http://localstack:4566/bucket/pic.png"

    mock_file = MagicMock()
    mock_file.filename = "tomato.png"
    mock_file.content_type = "image/png"
    mock_file.file = b"fake-image-data"

    result_url = service.handle_photo_upload(seedling_id=1, file=mock_file)

    mock_upload.assert_called_once_with(mock_file.file, "tomato.png", "image/png")
    
    mock_repo.update_image_urls.assert_called_once_with(1, image_url=result_url)
    
    mock_notify.assert_called_once_with(1, "tomato.png")
    
    assert result_url == "http://localstack:4566/bucket/pic.png"

def test_upload_photo_s3_failure(mocker):
    mocker.patch("app.services.seedling_service.upload_to_s3", side_effect=Exception("S3 Down"))
    
    mock_repo = MagicMock()
    mock_repo.get_by_id.return_value = MagicMock(id=1)
    
    service = SeedlingService(db=MagicMock())
    service.repo = mock_repo
    
    with pytest.raises(Exception) as excinfo:
        service.handle_photo_upload(seedling_id=1, file=MagicMock())
    
    assert "S3 Down" in str(excinfo.value)