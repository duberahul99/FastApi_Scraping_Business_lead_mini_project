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
        except Exception as e:
            print("SERP error:", e)
            return {}

    def enrich(self, candidate):
        api_key = os.getenv("SERP_API_KEY")

        # -----------------------------------
        # STEP 1 — SERP API (Google Maps Place Details)
        # -----------------------------------
        place_id = candidate.get("place_id_search")

        if place_id:
            params = {
                "engine": "google_maps",
                "type": "place",
                "place_id": place_id,
                "api_key": api_key
            }

            data = self.safe_request(params)
            place = data.get("place_results", {})

            candidate["official_site"] = place.get("website", "N/A")
            candidate["phone"] = place.get("phone", candidate.get("phone", "N/A"))
            candidate["address"] = place.get("address", candidate.get("address", "N/A"))

        # -----------------------------------
        # STEP 2 — Official Website via Knowledge Graph (fallback)
        # -----------------------------------
        if candidate.get("official_site") == "N/A" or candidate.get("phone") == "N/A":
            params = {
                "engine": "google",
                "q": f"{candidate.get('name')} {candidate.get('address')}",
                "api_key": api_key
            }

            data = self.safe_request(params)
            kg = data.get("knowledge_graph", {})

            if candidate.get("official_site") == "N/A":
                candidate["official_site"] = kg.get("website", "N/A")

            if candidate.get("phone") == "N/A":
                candidate["phone"] = kg.get("phone", "N/A")

        # -----------------------------------
        # STEP 3 — Social Media (last priority)
        # -----------------------------------
        params = {
            "engine": "google",
            "q": f"{candidate.get('name')} {candidate.get('address')} facebook instagram linkedin",
            "api_key": api_key
        }

        data = self.safe_request(params)
        organic = data.get("organic_results", [])

        candidate["facebook"] = "N/A"
        candidate["instagram"] = "N/A"
        candidate["linkedin"] = "N/A"

        for item in organic:
            link = item.get("link", "")
            if "facebook.com" in link and candidate["facebook"] == "N/A":
                candidate["facebook"] = link
            elif "instagram.com" in link and candidate["instagram"] == "N/A":
                candidate["instagram"] = link
            elif "linkedin.com/company" in link and candidate["linkedin"] == "N/A":
                candidate["linkedin"] = link

        return candidate
