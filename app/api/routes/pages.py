from fastapi import APIRouter
from fastapi.responses import FileResponse, HTMLResponse
from pathlib import Path

router = APIRouter(tags=["pages"])


@router.get("/standings", response_class=HTMLResponse)
def standings_form():
    """Serve the standings form HTML"""
    form_path = Path("app/static/standings_form.html")
    return form_path.read_text(encoding="utf-8")