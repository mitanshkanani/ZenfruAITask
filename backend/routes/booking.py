from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta   # <-- Added timedelta import
from utils.file_utils import read_json_file, write_json_file

router = APIRouter()

class BookingRequest(BaseModel):
    name: str
    doctor: str
    day: str
    slot: str  # e.g., "15:00"

@router.post("/log_booking")
async def log_booking(booking: BookingRequest):
    """
    Logs a booking to appointments.json
    """
    try:
        appointments = read_json_file("backend/data/appointments.json")

        today = datetime.today()
        target_day = booking.day.capitalize()
        weekday_map = {
            "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
            "Friday": 4, "Saturday": 5, "Sunday": 6
        }

        if target_day not in weekday_map:
            raise HTTPException(status_code=400, detail="Invalid day")

        target_weekday = weekday_map[target_day]
        days_ahead = (target_weekday - today.weekday() + 7) % 7
        if days_ahead == 0:
            days_ahead = 7  # always pick next week's day

        appointment_date = today + timedelta(days=days_ahead)

        # Combine date + time
        start_dt_str = f"{appointment_date.date()}T{booking.slot}:00"
        start_dt = datetime.fromisoformat(start_dt_str)
        end_dt = start_dt + timedelta(minutes=30)

        new_appt = {
            "name": booking.name,
            "start_time": start_dt.isoformat(),
            "end_time": end_dt.isoformat()
        }
        appointments.append(new_appt)

        write_json_file("backend/data/appointments.json", appointments)

        print(f"📅 New booking logged: {new_appt}")
        return {
            "status": "success",
            "message": f"Booking logged successfully for {booking.name} at {booking.slot} with {booking.doctor} on {booking.day}",
            "appointment": new_appt
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
