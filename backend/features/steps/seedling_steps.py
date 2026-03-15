import io
from behave import given, when, then
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

@given('the seedling API is running')
def step_impl(context):
    context.client = client
    
    context.mock_seedling_data = [{
        "crop_type": "mangoes",
        "quantity": 100,
        "location": "Kathanwa",
        "planting_date": "2026-02-14",
        "id": 1,
        "image_url": "http://host.docker.internal:4566/seedling-assets/derrick-pic.png",
        "thumbnail_url": "http://host.docker.internal:4566/seedling-assets/thumbnails/derrick-pic.png",
        "ready_date": "2026-05-15",
        "days_remaining": 90,
        "status": "Growing"
    }]

    # patch S3 and SQS to avoid connection errors
    context.s3_patch = patch("app.services.seedling_service.upload_to_s3", 
                             return_value=context.mock_seedling_data[0]["image_url"]).start()
    context.sqs_patch = patch("app.services.seedling_service.notify_worker").start()

    # patch the search service
    context.mocker_get = patch("app.services.seedling_service.SeedlingService.get_seedlings_with_status")
    context.mock_get = context.mocker_get.start()
    context.mock_get.return_value = context.mock_seedling_data


@when('I create a new seedling with crop "{crop}" and quantity {quantity:d}')
def step_impl(context, crop, quantity):
    payload = {
        "crop_type": crop,
        "quantity": quantity,
        "location": "Kathanwa",
        "planting_date": "2026-02-14",
        "maturity_days": 90
    }
    context.response = context.client.post("/seedlings/", json=payload)

@when('I upload a photo "{filename}" for this seedling')
def step_impl(context, filename):
    #io.BytesIO is better than raw strings for file streams
    file_stream = io.BytesIO(b"fake-image-content")
    file_data = {"file": (filename, file_stream, "image/jpeg")}
    
    url = f"/seedlings/{context.seedling_id}/upload-photo/"
    context.upload_response = context.client.post(url, files=file_data)

@when('I fetch the seedling details for this ID')
def step_impl(context):
    # Update mock identity to match the auto-incremented ID from the POST step
    context.mock_seedling_data[0]["id"] = context.seedling_id
    context.mock_get.return_value = context.mock_seedling_data

    query_params = {"query_date": "2026-02-14"}
    context.fetch_response = context.client.get("/buyers/search", params=query_params)

@then('the seedling should be created with an ID')
def step_impl(context):
    assert context.response.status_code == 200, f"Create failed: {context.response.text}"
    context.seedling_id = context.response.json()["id"]
    assert context.seedling_id is not None

@then('the seedling image URL should be updated')
def step_impl(context):
    assert context.upload_response.status_code == 200
    data = context.upload_response.json()
    assert data["status"] == "Uploaded & Processing"
    assert int(data["seedling_id"]) == int(context.seedling_id)

@then('the response should contain valid "{crop}" data with status "{status}"')
def step_impl(context, crop, status):
    results = context.fetch_response.json()
    assert isinstance(results, list)
    
    data = next((item for item in results if item["id"] == context.seedling_id), None)
    
    assert data is not None, f"Seedling ID {context.seedling_id} not found!"
    assert data["crop_type"] == crop
    assert data["status"] == status
    assert "seedling-assets" in data["image_url"]
    
    patch.stopall()