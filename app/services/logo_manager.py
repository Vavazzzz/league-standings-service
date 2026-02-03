from PIL import Image
from pathlib import Path


LOGO_DIR = Path("app/assets/logos")


def get_logo(team_name: str):
    return Image.open(LOGO_DIR / f"{team_name}.png")
