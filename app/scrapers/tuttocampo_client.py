import httpx


class TuttoCampoClient:

    HEADERS = {
        "User-Agent": "Mozilla/5.0",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.tuttocampo.it/"
    }

    async def fetch(self, url: str) -> str:
        async with httpx.AsyncClient(headers=self.HEADERS) as client:
            r = await client.get(url)
            r.raise_for_status()
            return r.text
