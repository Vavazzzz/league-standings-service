from json import loads

from pathlib import Path
from pydantic import BaseModel

from app.renderers.standings_renderer import StandingsRenderer


# Fake model identico a StandingRow
class FakeStanding(BaseModel):
    team_id: int
    team_name: str
    points: int
    played: int



def test_render_classifica(tmp_path):

    template = Path("app/assets/templates/template_classifica.svg")
    logos = Path("app/assets/logos")

    renderer = StandingsRenderer(template, logos)

    dummy_data = loads(Path("app/data/standings/giornata_14.json").read_text())

    output = tmp_path / "classifica.png"

    renderer.render_png(dummy_data, output)

    assert output.exists()
    assert output.stat().st_size > 0


if __name__ == "__main__":
    test_render_classifica(Path("test_output"))
