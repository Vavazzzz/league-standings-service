from pathlib import Path
from app.scrapers.standings_scraper import fetch_standings
from app.renderers.standings_renderer import StandingsRenderer


class StandingsRenderService:
    """Service that orchestrates standings scraping and rendering"""
    
    def __init__(self):
        self.template_path = Path("app/assets/templates/template_classifica.svg")
        self.logos_dir = Path("app/assets/logos")
        self.output_dir = Path("app/renderers/output")
        self.renderer = StandingsRenderer(self.template_path, self.logos_dir)
    
    def render_standings_png(self, team_id: str = "1", match_day: int | None = None) -> Path:
        """
        Fetch standings data and render as PNG.
        
        Args:
            team_id: Team ID (default: "1")
            match_day: Optional matchday number
            
        Returns:
            Path to the generated PNG file
            
        Raises:
            ValueError: If standings don't have exactly 12 teams
        """
        # Fetch standings from scraper
        standings_rows = fetch_standings(match_day, team_id)
        
        # Convert StandingRow objects to dictionaries for renderer
        standings_data = [
            {
                "position": row.position,
                "team_id": row.team_id,
                "team_name": row.team_name,
                "points": row.points,
                "played": row.played,
                "wins": row.wins,
                "draws": row.draws,
                "losses": row.losses,
                "goals_for": row.goals_for,
                "goals_against": row.goals_against,
                "goal_diff": row.goal_diff,
                "status": row.status
            }
            for row in standings_rows
        ]
        
        # Generate filename
        filename = self._generate_filename(team_id, match_day)
        output_path = self.output_dir / filename
        
        # Render PNG
        self.renderer.render_png(standings_data, output_path)
        
        return output_path
    
    def _generate_filename(self, team_id: str, match_day: int | None) -> str:
        """Generate a descriptive filename for the output PNG"""
        if match_day:
            return f"standings_team{team_id}_matchday{match_day}.png"
        return f"standings_team{team_id}_total.png"