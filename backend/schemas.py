from pydantic import BaseModel
from typing import Optional

class TimetableCreate(BaseModel):
    subject: str
    day: str
    start_time: str
    end_time: str
    room: Optional[str] = None

class TimetableResponse(TimetableCreate):
    id: int

    class Config:
        from_attributes = True