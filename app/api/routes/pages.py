from fastapi import APIRouter
from fastapi.responses import FileResponse, HTMLResponse
from pathlib import Path

router = APIRouter(tags=["pages"])


@router.get("/", response_class=HTMLResponse)
def home():
    """Serve the home page with service selection"""
    form_path = Path("app/static/index.html")
    return form_path.read_text(encoding="utf-8")


@router.get("/standings", response_class=HTMLResponse)
def standings_form():
    """Serve the standings form HTML"""
    form_path = Path("app/static/standings_form.html")
    return form_path.read_text(encoding="utf-8")


@router.get("/results", response_class=HTMLResponse)
def results_form():
    """Serve the results form HTML"""
    form_path = Path("app/static/results_form.html")
    return form_path.read_text(encoding="utf-8")


@router.get("/matchday", response_class=HTMLResponse)
def matchday_form():
    """Serve the matchday form HTML"""
    form_path = Path("app/static/matchday_form.html")
    return form_path.read_text(encoding="utf-8")