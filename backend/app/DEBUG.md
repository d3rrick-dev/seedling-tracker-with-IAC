### After updating image columns

```bash 
$ alembic revision --autogenerate -m "add_image_columns"                
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
ERROR [alembic.util.messaging] Target database is not up to date.
  FAILED: Target database is not up to date.

uv run alembic stamp head
uv run alembic revision --autogenerate -m "add_image_columns"
uv run alembic upgrade head

//local
uvicorn app.main:app --reload


curl -X POST "http://localhost:8000/seedlings/" \
     -H "Content-Type: application/json" \
     -d '{"crop_type": "avocado", "quantity": 10, "location": "Nairobi", "planting_date": "2024-03-20"}'

curl -X POST "http://localhost:8000/seedlings/1/upload-photo/" \
     -F "file=@plant.jpg"


$ kubectl logs -f deployment/seedling-worker -n farming-platform
INFO:worker:Worker started. Polling SQS...
INFO:worker:Success: Thumbnail for Seedling 1
INFO:worker:Success: Thumbnail for Seedling 5

{
  "id": 5,
  "crop_type": "avocado",
  "quantity": 10,
  "location": "Nairobi",
  "image_url": "http://host.docker.internal:4566/seedling-assets/derrick-pic.png",
  "thumbnail_url": "http://host.docker.internal:4566/seedling-assets/thumbnails/derrick-pic.png",
  "ready_date": "2024-08-17",
  "days_remaining": 0,
  "status": "Ready"
}

```