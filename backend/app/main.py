from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from datetime import date, timedelta
from . import models, schemas, database

app = FastAPI(title="Seedling Tracker API")


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/seedlings/", response_model=schemas.SeedlingOut)
def create_seedling(seedling: schemas.SeedlingCreate, db: Session = Depends(get_db)):
    db_seedling = models.Seedling(**seedling.model_dump())
    db.add(db_seedling)
    db.commit()
    db.refresh(db_seedling)
    return db_seedling

@app.get("/buyers/search/")
def search_seedlings(query_date: date = Query(...), db: Session = Depends(get_db)):
    seedlings = db.query(models.Seedling).all()
    results = []

    for s in seedlings:
        ready_date = s.planting_date + timedelta(days=s.maturity_days)
        days_remaining = (ready_date - query_date).days
        
        results.append({
            "id": s.id,
            "crop_type": s.crop_type,
            "quantity": s.quantity,
            "location": s.location,
            "ready_date": ready_date,
            "days_remaining": max(0, days_remaining),
            "status": "Ready" if days_remaining <= 0 else "Growing"
        })
    
    return results