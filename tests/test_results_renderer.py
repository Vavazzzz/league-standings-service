from pathlib import Path
from app.renderers.results_renderer import ResultRenderer


def test_render_result():

    renderer = ResultRenderer(
        template_path=Path("app/assets/templates/template_risultato_doppio.svg"),
        logos_dir=Path("app/assets/logos")
    )

    dummy_1 = {
        "match_day": 14,
        "date": "Gio. 29 gennaio",
        "time": "21:15",
        "home_team": "Polpenazze",
        "home_team_id": 1016296,
        "away_team": "Zelo Co5",
        "away_team_id": 1026114,
        "home_score": 3,
        "away_score": 6,
        "home_scorers": [
            {"name": "D. Ferreyra"},
            {"name": "M. Sarr"},
            {"name": "C. Miloni (11' pt)"}
        ],
        "away_scorers": [
            {"name": "M. Di Biasi"},
            {"name": "S. Rebuscini"},
            {"name": "R. Scaglione"},
            {"name": "L. De Morais"},
            {"name": "L. Passaretta"},
            {"name": "O. Ceroni"}
        ]
    }

    dummy_2 = {
  "match_day": 12,
  "date": "Gio. 29 gennaio",
  "time": "22:00",
  "home_team": "Movisport",
  "home_team_id": 1199860,
  "away_team": "Zelo C5 U23",
  "away_team_id": 1288835,
  "home_score": 4,
  "away_score": 4,
  "home_scorers": [
    {
      "name": "L. Ghiglia",
      "player_id": 9523120
    },
    {
      "name": "L. Ghiglia",
      "player_id": 9523120
    },
    {
      "name": "L. Ghiglia",
      "player_id": 9523120
    },
    {
      "name": "G. Zuzzè",
      "player_id": 10331139
    }
  ],
  "away_scorers": [
    {
      "name": "M. Re",
      "player_id": 8914057
    },
    {
      "name": "N. Esposti",
      "player_id": 9636054
    },
    {
      "name": "A. Gelmi",
      "player_id": 7597871
    },
    {
      "name": "A. Gelmi",
      "player_id": 7597871
    }
  ]
}
    
    renderer.render_png(dummy_1, dummy_2, Path("test_output/result.png"))

if __name__ == "__main__":
    test_render_result()