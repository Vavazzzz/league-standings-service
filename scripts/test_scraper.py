import asyncio

from app.scrapers.ranking_scraper import StandingsScraper
from app.scrapers.matchday_scraper import MatchdayScraper


STANDINGS_URL = "https://www.tuttocampo.it/Lombardia/CalcioA5SerieC2/GironeBSerieC2/Giornata14"
MATCHDAY_URL = "https://www.tuttocampo.it/Lombardia/CalcioA5SerieC2/GironeBSerieC2/Giornata14"

async def main():
    standings = await StandingsScraper().scrape(STANDINGS_URL)

    print("\nCLASSIFICA")
    for t in standings.teams:
        print(t)

    matches = await MatchdayScraper().scrape(MATCHDAY_URL)

    print("\nMATCHDAY")
    for m in matches:
        print(m)


if __name__ == "__main__":
    asyncio.run(main())
