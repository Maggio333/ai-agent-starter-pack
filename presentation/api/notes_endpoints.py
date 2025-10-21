from fastapi import APIRouter, Form
from typing import Optional, Dict, Any

router = APIRouter()


@router.post("/notes/save")
async def save_note(
    title: str = Form(...),
    content: str = Form(...),
    date_iso: Optional[str] = Form(default=None),
    location: Optional[str] = Form(default=None),
    tags: Optional[str] = Form(default=""),
) -> Dict[str, Any]:
    # Skeleton: later persist to SQLite/Markdown
    return {
        "status": "ok",
        "saved": True,
        "title": title,
        "date": date_iso,
        "location": location,
        "tags": [t.strip() for t in tags.split(",") if t.strip()],
    }

