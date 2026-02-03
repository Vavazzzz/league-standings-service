import requests


class TuttoCampoClient:
    """Client per TuttoCampo che mantiene la sessione e i cookies"""
    
    BASE_URL = "https://www.tuttocampo.it"
    CATEGORY_ID = "LO.K.B.S2"
    
    def __init__(self):
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
            
        main_url = f"{self.BASE_URL}/Lombardia/CalcioA5SerieC2/GironeBSerieC2"
        
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
            "category_id": self.CATEGORY_ID,
            "match_day_id": match_day or "",
            "total": "true",
            "is_ranking_tab": "false"
        }
        
        url = f"{self.BASE_URL}/Web/Views/Rankings/RankingView.php"
        response = self.session.get(url, params=params, headers=self.headers, timeout=10)
        response.raise_for_status()
        return response.text

    def fetch_results(self, match_day: int) -> str:
        """Fetcha i risultati per una giornata specifica"""
        self._initialize_session()
        
        params = {
            "tckk": self.tckk,
            "v": "1",
            "category_id": self.CATEGORY_ID,
            "match_day_id": match_day,
            "is_ranking_tab": "false"
        }
        
        url = f"{self.BASE_URL}/Web/Views/Results/ResultsView.php"
        response = self.session.get(url, params=params, headers=self.headers, timeout=10)
        response.raise_for_status()
        return response.text

    def fetch_next_matches(self, match_day: int) -> str:
        """Fetcha le prossime partite per una giornata specifica"""
        # È lo stesso endpoint dei risultati, ma potrebbe essere filtrato diversamente
        return self.fetch_results(match_day)
