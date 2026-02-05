import requests
import os

class Enricher:

    def safe_request(self, params):
        try:
            res = requests.get(
                "https://serpapi.com/search.json",
                params=params,
                timeout=8
            )
            return res.json()
        except:
            return {}

    def enrich(self, candidate):
        api_key = os.getenv("SERP_API_KEY")

        params = {
            "engine": "google",
            "q": f"{candidate.get('name')} {candidate.get('address')}",
            "api_key": api_key
        }

        data = self.safe_request(params)
        kg = data.get("knowledge_graph", {})

        candidate["official_site"] = kg.get("website", "N/A")
        candidate["phone"] = kg.get("phone", candidate.get("phone", "N/A"))
        candidate["address"] = kg.get("address", candidate.get("address"))

        return candidate
