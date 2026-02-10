from pathlib import Path
import tempfile
import cairosvg
from lxml import etree as ET

from app.renderers.svg_utils import load_svg, set_logo
from app.renderers.text_utils import set_text, extract_surnames, set_multiline_text


class ResultRenderer:

    def __init__(self, template_path: Path, logos_dir: Path):
        self.template_path = template_path
        self.logos_dir = logos_dir

    def render_png(self, match_data_1: dict, match_data_2: dict, output_path: Path):

        root = load_svg(str(self.template_path))

        # ===== risultato =====

        set_text(root, "home_score_1", match_data_1["home_score"])
        set_text(root, "away_score_1", match_data_1["away_score"])
        set_text(root, "home_score_2", match_data_2["home_score"])
        set_text(root, "away_score_2", match_data_2["away_score"])

        # ===== loghi =====

        set_logo(root, "home_logo_1", self.logos_dir / f"{match_data_1['home_team_id']}.png")
        set_logo(root, "away_logo_1", self.logos_dir / f"{match_data_1['away_team_id']}.png")
        set_logo(root, "home_logo_2", self.logos_dir / f"{match_data_2['home_team_id']}.png")
        set_logo(root, "away_logo_2", self.logos_dir / f"{match_data_2['away_team_id']}.png")

        # ===== marcatori =====

        scorers_1_data = (
            match_data_1["home_scorers"]
            if match_data_1["home_team"] == "Zelo CO5"
            else match_data_1["away_scorers"]
        )

        scorers_2_data = (
            match_data_2["home_scorers"]
            if match_data_2["home_team"] == "Zelo C5 U23"
            else match_data_2["away_scorers"]
        )

        set_multiline_text(root, "scorers_1", extract_surnames(scorers_1_data))
        set_multiline_text(root, "scorers_2", extract_surnames(scorers_2_data))

        # ===== salva svg temporaneo =====

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as tmp:
            ET.ElementTree(root).write(tmp.name)
            temp_svg = tmp.name

        output_path.parent.mkdir(parents=True, exist_ok=True)

        # ===== export png =====

        cairosvg.svg2png(
            url=temp_svg,
            write_to=str(output_path),
            output_width=1600,
            output_height=1600,
            unsafe=True
        )
