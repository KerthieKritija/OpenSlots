from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models
import schemas

app = FastAPI()

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "OpenSlots Backend Running"}

# Create timetable entry
@app.post("/timetable", response_model=schemas.TimetableResponse)
def create_entry(entry: schemas.TimetableCreate, db: Session = Depends(get_db)):
    db_entry = models.TimetableEntry(**entry.model_dump())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

# Get all timetable entries
@app.get("/timetable")
def get_entries(db: Session = Depends(get_db)):
    return db.query(models.TimetableEntry).all()