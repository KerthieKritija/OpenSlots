from sqlalchemy import Column, Integer, String
from database import Base

class TimetableEntry(Base):
    __tablename__ = "timetable"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, nullable=False)
    day = Column(String, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    room = Column(String, nullable=True)