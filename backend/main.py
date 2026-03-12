from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from datetime import datetime
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
@app.get("/free-slots/{day}")
def get_free_slots(day: str, db: Session = Depends(get_db)):
    entries = db.query(models.TimetableEntry).filter(
        models.TimetableEntry.day == day
    ).all()

    if not entries:
        return {"message": "No classes found for this day"}

    # convert times to datetime objects
    time_blocks = []
    for entry in entries:
        start = datetime.strptime(entry.start_time, "%H:%M")
        end = datetime.strptime(entry.end_time, "%H:%M")
        time_blocks.append((start, end))

    # sort classes by start time
    time_blocks.sort(key=lambda x: x[0])

    free_slots = []

    day_start = datetime.strptime("09:00", "%H:%M")
    day_end = datetime.strptime("17:00", "%H:%M")

    # gap before first class
    if time_blocks[0][0] > day_start:
        free_slots.append({
            "start": day_start.strftime("%H:%M"),
            "end": time_blocks[0][0].strftime("%H:%M")
        })

    # gaps between classes
    for i in range(len(time_blocks)-1):
        current_end = time_blocks[i][1]
        next_start = time_blocks[i+1][0]

        if next_start > current_end:
            free_slots.append({
                "start": current_end.strftime("%H:%M"),
                "end": next_start.strftime("%H:%M")
            })

    # gap after last class
    if time_blocks[-1][1] < day_end:
        free_slots.append({
            "start": time_blocks[-1][1].strftime("%H:%M"),
            "end": day_end.strftime("%H:%M")
        })

    return {
        "day": day,
        "free_slots": free_slots
    }