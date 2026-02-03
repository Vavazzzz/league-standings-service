from fastapi import APIRouter, Query
from fastapi.responses import FileResponse
from app.services.standings_service import generate_standings_image

router = APIRouter(prefix="/standings", tags=["standings"])


@router.get("/")
def get_standings(matchday: int = Query(...)):
    file_path = generate_standings_image(matchday)
    return FileResponse(file_path, media_type="image/png")
