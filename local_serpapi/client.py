import requests
import os
from dotenv import load_dotenv

load_dotenv()

class SerpApiClient:
    def __init__(self):
        self.api_key = os.getenv("SERP_API_KEY")
        self.url = "https://serpapi.com/search.json"

    def search(self, niche, location, limit):
        params = {
            "engine": "google_maps",
            "type": "search",
            "q": f"{niche} in {location}",
            "hl": "en",
            "api_key": self.api_key
        }

        try:
            res = requests.get(self.url, params=params, timeout=10)
            data = res.json()
            places = data.get("local_results", [])
        except Exception as e:
            print("Maps error:", e)
            return []

        results = []
        for p in places:
            results.append({
                "name": p.get("title"),
                "address": p.get("address", "N/A"),
                "phone": p.get("phone", "N/A"),
                "official_site": "N/A",
                "facebook": "N/A",
                "instagram": "N/A",
                "linkedin": "N/A",
                "place_id_search": p.get("place_id")
            })

        return results[:limit]
