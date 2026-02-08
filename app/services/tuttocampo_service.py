from scrapers.tuttocampo_client import TuttoCampoClient
from app.scrapers.standings_scraper import parse_ranking
from scrapers.result_scraper import parse_results


class TuttoCampoService:

    def __init__(self):
        self.client = TuttoCampoClient()

    async def get_ranking(self, url: str):
        html = await self.client.fetch(url)
        return parse_ranking(html)

    async def get_results(self, url: str):
        html = await self.client.fetch(url)
        return parse_results(html)
