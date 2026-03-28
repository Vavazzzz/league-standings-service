import requests
from app.core.config import settings

CATEGORY_ID_1 = "LO.K.B.S2"
CATEGORY_ID_2 = "LO.KD.A.SD"
URL_1 = "/Lombardia/CalcioA5SerieC2/GironeBSerieC2/"
URL_2 = "/Lombardia/CalcioA5Dilettanti/GironeASerieD/"

class TuttoCampoClient:
    """Client per TuttoCampo che mantiene la sessione e i cookies"""
    
    def __init__(self, team_id: str = "1"):
        """
        Initialize the TuttoCampo client for a specific team.
        
        Args:
            team_id: Team identifier matching TEAM<id> prefix in .env (default: "1")
        """
        # Load configuration from settings
        team_config = settings.get_team_config(team_id)
        
        self.base_url = team_config["base_url"]
        self.category_id = team_config["category_id"]
        self.main_url_path = team_config["main_url_path"]
        self.team_id = team_id
        
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "it-IT,it;q=0.9",
            "X-Requested-With": "XMLHttpRequest"
        }
        self.tckk = None
        self._initialized = False

    def _initialize_session(self):
        """Inizializza la sessione accedendo alla pagina principale"""
        if self._initialized:
            return
            
        main_url = f"{self.base_url}/{self.main_url_path}"
        
        try:
            response = self.session.get(main_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Estrai il tckk dalla pagina
            import re
            match = re.search(r'tckk=([a-f0-9]+)', response.text)
            if match:
                self.tckk = match.group(1)
            
            self._initialized = True
        except Exception as e:
            raise Exception(f"Errore durante l'inizializzazione della sessione: {e}")

    def fetch_standings(self, match_day: int | None = None) -> str:
        """Fetcha la classifica (standings) per una giornata specifica o totale"""
        self._initialize_session()
        
        params = {
            "tckk": self.tckk,
            "v": "1",
            "category_id": self.category_id,
            "match_day_id": match_day or "",
            "total": "true",
            "is_ranking_tab": "false"
        }
        
        url = f"{self.base_url}/Web/Views/Rankings/RankingView.php"
        response = self.session.get(url, params=params, headers=self.headers, timeout=10)
        response.raise_for_status()
        return response.text

    def fetch_results(self, match_day: int) -> str:
        """Fetcha i risultati per una giornata specifica"""
        self._initialize_session()
        
        params = {
            "tckk": self.tckk,
            "v": "1",
            "category_id": self.category_id,
            "match_day_id": match_day,
            "is_ranking_tab": "false"
        }
        
        url = f"{self.base_url}/Web/Views/Results/ResultsView.php"
        response = self.session.get(url, params=params, headers=self.headers, timeout=10)
        response.raise_for_status()
        return response.text

    def fetch_next_matches(self, match_day: int) -> str:
        """Fetcha le prossime partite per una giornata specifica"""
        return self.fetch_results(match_day)