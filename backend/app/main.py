from datetime import date
from fastapi import FastAPI, Depends, Query, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import schemas
from .database import get_db
from .services.seedling_service import SeedlingService

app = FastAPI(title="Seedling Tracker API")     

def get_seedling_service(db: Session = Depends(get_db)):
    return SeedlingService(db)

@app.post("/seedlings/", response_model=schemas.SeedlingOut)
def create_seedling(data: schemas.SeedlingCreate, service: SeedlingService = Depends(get_seedling_service)):
    """Register a new seedling."""
    return service.register_new_seedling(data)

@app.post("/seedlings/{seedling_id}/upload-photo/")
async def upload_photo(seedling_id: int, file: UploadFile = File(...), service: SeedlingService = Depends(get_seedling_service)):
    """Uploads a photo to S3, updates the DB, and triggers the thumbnail worker via Service."""

    try:
        result = service.handle_photo_upload(seedling_id, file)
        if not result:
            raise HTTPException(status_code=404, detail="Seedling not found")
        
        return {
            "status": "Uploaded & Processing", 
            "seedling_id": seedling_id,
            "image_url": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing Error: {str(e)}")

@app.get("/buyers/search/", response_model=List[schemas.SeedlingSearchOut])
def search_seedlings(query_date: date = Query(...), service: SeedlingService = Depends(get_seedling_service)):
    """Search for seedlings and calculate growth status via Service."""
    return service.get_seedlings_with_status(query_date)