# backend/models/booking_model.py
from pydantic import BaseModel


class BookingRequest(BaseModel):
    name: str
    doctor: str
    day: str       # e.g., "Saturday"
    slot: str      # e.g., "15:00"
