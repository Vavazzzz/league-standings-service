from PIL import Image
from app.services.logo_manager import get_logo


def render_image(standings, output_path):
    base = Image.open("app/assets/templates/base.png")

    for idx, team in enumerate(standings):
        logo = get_logo(team["name"])

        # posizione dinamica esempio
        base.paste(logo, (50, 100 + idx * 80), logo)

    base.save(output_path)
