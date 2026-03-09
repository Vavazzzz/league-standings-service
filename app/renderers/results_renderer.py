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

        # ===== Scores =====
        set_text(root, "home_score_1", match_data_1["home_score"])
        set_text(root, "away_score_1", match_data_1["away_score"])
        set_text(root, "home_score_2", match_data_2["home_score"])
        set_text(root, "away_score_2", match_data_2["away_score"])

        # ===== Logos =====
        set_logo(root, "home_logo_1", self.logos_dir / f"{match_data_1['home_team_id']}.png")
        set_logo(root, "away_logo_1", self.logos_dir / f"{match_data_1['away_team_id']}.png")
        set_logo(root, "home_logo_2", self.logos_dir / f"{match_data_2['home_team_id']}.png")
        set_logo(root, "away_logo_2", self.logos_dir / f"{match_data_2['away_team_id']}.png")

        # ===== Scorers =====
        # Extract scorers with just surnames
        home_scorers_1 = extract_surnames(match_data_1["home_scorers"])
        away_scorers_1 = extract_surnames(match_data_1["away_scorers"])
        home_scorers_2 = extract_surnames(match_data_2["home_scorers"])
        away_scorers_2 = extract_surnames(match_data_2["away_scorers"])
        
        # Use the team with more scorers
        scorers_1 = home_scorers_1 if len(home_scorers_1) >= len(away_scorers_1) else away_scorers_1
        scorers_2 = home_scorers_2 if len(home_scorers_2) >= len(away_scorers_2) else away_scorers_2
        
        set_multiline_text(root, "scorers_1", scorers_1)
        set_multiline_text(root, "scorers_2", scorers_2)

        # ===== Save temporary SVG =====
        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as tmp:
            ET.ElementTree(root).write(tmp.name)
            temp_svg = tmp.name

        output_path.parent.mkdir(parents=True, exist_ok=True)

        # ===== Export PNG =====
        cairosvg.svg2png(
            url=temp_svg,
            write_to=str(output_path),
            output_width=1600,
            output_height=1600,
            unsafe=True
        )