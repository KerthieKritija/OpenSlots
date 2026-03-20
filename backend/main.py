from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models
import schemas
from utils import find_free_slots

app = FastAPI()

# ✅ CORS FIX (IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend (localhost:3000)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "OpenSlots Backend Running"}


@app.post("/timetable", response_model=schemas.TimetableResponse)
def create_entry(entry: schemas.TimetableCreate, db: Session = Depends(get_db)):
    db_entry = models.TimetableEntry(**entry.model_dump())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


@app.get("/timetable")
def get_entries(db: Session = Depends(get_db)):
    return db.query(models.TimetableEntry).all()


# ✅ FREE SLOTS API
@app.get("/free-slots")
def get_free_slots(db: Session = Depends(get_db)):
    entries = db.query(models.TimetableEntry).all()
    return find_free_slots(entries)
