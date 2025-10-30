# backend/utils/slot_utils.py
import json
from datetime import datetime, timedelta
from backend.utils.file_utils import read_json_file

LUNCH_START = "13:00"
LUNCH_END = "14:00"
SLOT_DURATION_MINUTES = 30  # Each appointment is 30 minutes


def time_to_datetime(time_str: str) -> datetime:
    return datetime.strptime(time_str, "%H:%M")


def datetime_to_str(dt: datetime) -> str:
    return dt.strftime("%H:%M")


def generate_slots(start_time: str, end_time: str) -> list:
    """Generate 30-min slots between start_time and end_time"""
    slots = []
    start_dt = time_to_datetime(start_time)
    end_dt = time_to_datetime(end_time)

    while start_dt + timedelta(minutes=SLOT_DURATION_MINUTES) <= end_dt:
        slots.append(datetime_to_str(start_dt))
        start_dt += timedelta(minutes=SLOT_DURATION_MINUTES)

    return slots


def remove_lunch_slots(slots: list) -> list:
    """Remove slots that fall within the lunch break"""
    return [slot for slot in slots if slot < LUNCH_START or slot >= LUNCH_END]


def remove_booked_slots(slots: list, day: str, appointments: list) -> list:
    """Remove slots already booked on this day"""
    filtered = []
    for slot in slots:
        slot_dt = datetime.strptime(slot, "%H:%M")
        overlap = False
        for appt in appointments:
            appt_dt = datetime.fromisoformat(appt["start_time"])
            if appt_dt.strftime("%A") == day:
                appt_start = appt_dt
                appt_end = appt_dt + timedelta(minutes=SLOT_DURATION_MINUTES)
                if appt_start.time() <= slot_dt.time() < appt_end.time():
                    overlap = True
                    break
        if not overlap:
            filtered.append(slot)
    return filtered


def get_available_slots(day: str) -> dict:
    """
    Returns available slots and doctor for a given day.
    """
    # Load schedules
    schedules = read_json_file("backend/data/schedules.json")
    if day not in schedules:
        raise ValueError(f"Invalid day: {day}")

    doctor = schedules[day]["doctor"]
    start_time = schedules[day]["start_time"]
    end_time = schedules[day]["end_time"]

    # Generate all slots in working hours
    slots = generate_slots(start_time, end_time)

    # Remove lunch break slots
    slots = remove_lunch_slots(slots)

    # Load appointments
    appointments = read_json_file("backend/data/appointments.json")

    # Remove already booked slots
    slots = remove_booked_slots(slots, day, appointments)

    return {"doctor": doctor, "available_slots": slots}
