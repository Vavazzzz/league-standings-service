from app.scrapers.ranking_scraper import parse_ranking
import requests
import re

# URL della pagina principale
STANDINGS_URL = "https://www.tuttocampo.it/Lombardia/CalcioA5SerieC2/GironeBSerieC2/Giornata14"

def test_ranking_scraper():
    """Testa lo scraper della classifica con sessione e cookies"""
    
    print("=" * 80)
    print("TEST SCRAPER CLASSIFICA")
    print("=" * 80)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "it-IT,it;q=0.9"
    }
    
    # Usa una sessione per mantenere i cookies (PHPSESSID)
    session = requests.Session()
    
    try:
        print(f"\n[1] Accesso a pagina principale per ottenere PHPSESSID...")
        response = session.get(STANDINGS_URL, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"✗ Errore HTTP: {response.status_code}")
            return
            
        html_content = response.text
        print(f"✓ Pagina principale ricevuta ({len(html_content)} caratteri)")
        
        # Stampa i cookies ricevuti
        print(f"✓ Cookies nella sessione: {dict(session.cookies)}")
        
        # Estrai l'URL del rankingview.php dalla pagina
        print("\n[2] Estrazione parametri rankingview.php...")
        pattern = r'src=["\']([^"\']*RankingView\.php[^"\']*)["\']'
        matches = re.findall(pattern, html_content)
        
        ranking_url = None
        if matches:
            ranking_url = matches[0]
            if ranking_url.startswith('/'):
                ranking_url = 'https://www.tuttocampo.it' + ranking_url
            print(f"✓ URL trovato: {ranking_url}")
        else:
            # Se non trova tramite regex, usa l'URL noto
            print("ℹ URL non trovato via regex, uso URL noto")
            ranking_url = "https://www.tuttocampo.it/Web/Views/Rankings/RankingView.php?tckk=8ce24aa6b00a597f2d98b4fe6e8b29c6ed1eae0c&v=1&category_id=LO.K.B.S2&match_day_id=&total=true&is_ranking_tab=false"
        
        # Prepara headers per la richiesta al rankingview.php
        ranking_headers = headers.copy()
        ranking_headers["Referer"] = STANDINGS_URL
        ranking_headers["X-Requested-With"] = "XMLHttpRequest"
        
        print(f"\n[3] Accesso a rankingview.php con PHPSESSID...")
        response = session.get(ranking_url, headers=ranking_headers, timeout=10)
        
        print(f"Status code: {response.status_code}")
        print(f"Content length: {len(response.text)}")
        
        if response.status_code == 200:
            ranking_html = response.text
            print(f"✓ Risposta ricevuta ({len(ranking_html)} caratteri)")
            
            # Debug: stampa primo chunk dell'HTML
            print(f"\nPrimi 500 caratteri della risposta:")
            print(ranking_html[:500])
            
            print("\n[4] Parsing della classifica...")
            standings = parse_ranking(ranking_html)
            
            if standings:
                print(f"✓ {len(standings)} squadre trovate\n")
                print("Classifica:")
                print("-" * 120)
                for standing in standings:
                    print(f"{standing.position:2d}. {standing.team_name:25s} | Pt: {standing.points:3d} | "
                          f"G: {standing.played:2d} | V: {standing.wins:2d} | "
                          f"N: {standing.draws:2d} | P: {standing.losses:2d} | "
                          f"GF: {standing.goals_for:2d} | GC: {standing.goals_against:2d} | "
                          f"Diff: {standing.goal_diff:3d}")
            else:
                print("✗ Nessuna squadra trovata")
                print("\nHTML completo della risposta:")
                print(ranking_html)
        else:
            print(f"✗ Errore HTTP rankingview.php: {response.status_code}")
            print(f"Risposta: {response.text[:1000]}")
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Errore di connessione: {e}")
    except Exception as e:
        print(f"✗ Errore: {e}")
        import traceback
        traceback.print_exc()
            
if __name__ == "__main__":
    test_ranking_scraper()