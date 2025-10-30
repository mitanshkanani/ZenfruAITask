# backend/routes/info.py
from fastapi import APIRouter, Query, HTTPException
from utils.file_utils import read_json_file

router = APIRouter()


@router.get("/get_info")
async def get_info(topic: str = Query(..., description="Query topic: 'hours', 'doctors', 'services', 'walk_in'")):
    """
    Returns clinic info based on the requested topic.
    """
    try:
        knowledge_base = read_json_file("backend/data/knowledge_base.json")

        topic = topic.lower()
        if topic == "hours":
            return {"clinic_hours": knowledge_base.get("clinic_hours", "Not available")}
        elif topic == "doctors":
            return {"doctors": knowledge_base.get("doctors", {})}
        elif topic == "services":
            return {"services": knowledge_base.get("faq", {}).get("services", [])}
        elif topic == "walk_in":
            return {"walk_in": knowledge_base.get("faq", {}).get("walk_in", "Not available")}
        else:
            raise HTTPException(
                status_code=400, detail=f"Unknown topic: {topic}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
