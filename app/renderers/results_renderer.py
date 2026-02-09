from pathlib import Path
import tempfile
import cairosvg

from app.renderers.svg_utils import (
    load_svg,
    set_text,
    set_logo
)

from app.renderers.text_utils import extract_surnames, set_multiline_text


class ResultRenderer:

    def __init__(self, template_path: Path, logos_dir: Path):
        self.template_path = template_path
        self.logos_dir = logos_dir

    def render_png(self, match_data_1: dict, match_data_2: dict, output_path: Path):

        tree = load_svg(str(self.template_path))

        # ===== risultato =====

        set_text(tree, "home_score_1", match_data_1["home_score"])
        set_text(tree, "away_score_1", match_data_1["away_score"])
        set_text(tree, "home_score_2", match_data_2["home_score"])
        set_text(tree, "away_score_2", match_data_2["away_score"])

        # ===== loghi =====

        home_logo_1 = self.logos_dir / f"{match_data_1['home_team_id']}.png"
        away_logo_1 = self.logos_dir / f"{match_data_1['away_team_id']}.png"
        home_logo_2 = self.logos_dir / f"{match_data_2['home_team_id']}.png"
        away_logo_2 = self.logos_dir / f"{match_data_2['away_team_id']}.png"

        set_logo(tree, "home_logo_1", str(home_logo_1))
        set_logo(tree, "away_logo_1", str(away_logo_1))
        set_logo(tree, "home_logo_2", str(home_logo_2))
        set_logo(tree, "away_logo_2", str(away_logo_2))

        # ===== marcatori multiline =====

        scorers_1 = extract_surnames(match_data_1["home_scorers"])
        scorers_2 = extract_surnames(match_data_2["home_scorers"])
        
        set_multiline_text(tree, "scorers_1", scorers_1)
        set_multiline_text(tree, "scorers_2", scorers_2)
  
        # ===== salva svg temporaneo =====

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as tmp:
            tree.write(tmp.name)
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
