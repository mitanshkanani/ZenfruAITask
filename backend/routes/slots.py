# backend/routes/slots.py
from fastapi import APIRouter, HTTPException, Query
from backend.utils.slot_utils import get_available_slots

router = APIRouter()


@router.get("/get_slots")
async def get_slots(day: str = Query(..., description="Day of the week, e.g., Monday")):
    """
    Returns available slots for the requested day along with the assigned doctor.
    """
    try:
        slots_data = get_available_slots(day)
        return slots_data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
