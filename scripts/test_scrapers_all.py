"""
Test script per verificare che gli scraper funzionano correttamente
"""

from app.scrapers.ranking_scraper import fetch_standings
from app.scrapers.result_scraper import fetch_results
from app.scrapers.matchday_scraper import fetch_next_matches

def test_standings():
    """Test classifica totale"""
    print("\n" + "="*80)
    print("TEST: Classifica Totale")
    print("="*80)
    
    try:
        standings = fetch_standings()
        print(f"✓ {len(standings)} squadre trovate\n")
        
        print("Top 5 Classifica:")
        print("-" * 100)
        for standing in standings[:5]:
            print(f"{standing.position:2d}. {standing.team_name:25s} | Pt: {standing.points:3d} | "
                  f"G: {standing.played:2d} | GF: {standing.goals_for:2d} | "
                  f"GC: {standing.goals_against:2d} | Diff: {standing.goal_diff:3d}")
    except Exception as e:
        print(f"✗ Errore: {e}")
        import traceback
        traceback.print_exc()


def test_standings_by_matchday():
    """Test classifica per giornata"""
    print("\n" + "="*80)
    print("TEST: Classifica Giornata 5")
    print("="*80)
    
    try:
        standings = fetch_standings(match_day=5)
        print(f"✓ {len(standings)} squadre trovate\n")
        
        print("Classifica Giornata 5:")
        print("-" * 100)
        for standing in standings[:5]:
            print(f"{standing.position:2d}. {standing.team_name:25s} | Pt: {standing.points:3d} | "
                  f"G: {standing.played:2d} | GF: {standing.goals_for:2d} | "
                  f"GC: {standing.goals_against:2d} | Diff: {standing.goal_diff:3d}")
    except Exception as e:
        print(f"✗ Errore: {e}")
        import traceback
        traceback.print_exc()


def test_results():
    """Test risultati giornata"""
    print("\n" + "="*80)
    print("TEST: Risultati Giornata 14")
    print("="*80)
    
    try:
        results = fetch_results(match_day=14)
        print(f"✓ {len(results)} partite trovate\n")
        
        print("Risultati:")
        print("-" * 100)
        for result in results:
            status = f"{result.home_score}-{result.away_score}" if result.home_score is not None else "In programma"
            print(f"{result.home_team:20s} {status:6s} {result.away_team:20s} | {result.date} {result.time or ''}")
    except Exception as e:
        print(f"✗ Errore: {e}")
        import traceback
        traceback.print_exc()


def test_matchday():
    """Test dati giornata completi"""
    print("\n" + "="*80)
    print("TEST: Dati Giornata 14")
    print("="*80)
    
    try:
        matchday = fetch_next_matches(match_day=14)
        print(f"✓ Giornata {matchday.match_day} con {len(matchday.matches)} partite\n")
        
        print("Partite:")
        print("-" * 100)
        for match in matchday.matches:
            status = f"{match.home_score}-{match.away_score}" if match.home_score is not None else "In programma"
            print(f"{match.home_team:20s} {status:6s} {match.away_team:20s} | {match.date} {match.time or ''}")
    except Exception as e:
        print(f"✗ Errore: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_standings()
    test_standings_by_matchday()
    test_results()
    test_matchday()
