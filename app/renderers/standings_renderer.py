from pathlib import Path
import tempfile

import cairosvg

from app.renderers.svg_utils import (
    load_svg,
    set_text,
    set_logo
)


class StandingsRenderer:

    def __init__(self, template_path: Path, logos_dir: Path):
        self.template_path = template_path
        self.logos_dir = logos_dir

    def render_png(self, standings: list, output_path: Path):

        if len(standings) != 12:
            raise ValueError("Il renderer classifica richiede esattamente 12 squadre")

        tree = load_svg(str(self.template_path))

        for team in standings:
            print(type(team), team)
            # ===== TESTO =====
            set_text(tree, f"row_{team['position']}_team", team['team_name'])
            set_text(tree, f"row_{team['position']}_giocate", team['played'])
            set_text(tree, f"row_{team['position']}_punti", team['points'])

            # ===== LOGO =====
            #logo_file = self.logos_dir / f"{team['team_id']}.png"

            #if not logo_file.exists():
                #raise FileNotFoundError(f"Logo mancante: {logo_file}")

            #set_logo(
                #ree,
                #f"row_{team['position']}_logo",
                #str(logo_file)
            #)

        # ===== salva svg temporaneo =====
        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as tmp:
            tree.write(tmp.name)
            temp_svg = tmp.name

        output_path.parent.mkdir(parents=True, exist_ok=True)

        # ===== export PNG =====
        cairosvg.svg2png(
            url=temp_svg,
            write_to=str(output_path),
            output_width=1600,
            output_height=1600
        )
