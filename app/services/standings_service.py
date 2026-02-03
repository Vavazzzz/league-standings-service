from app.services.image_renderer import render_image
from app.data_loader import load_standings


def generate_standings_image(matchday: int):
    standings = load_standings(matchday)
    output_path = f"/tmp/standings_{matchday}.png"

    render_image(standings, output_path)

    return output_path
