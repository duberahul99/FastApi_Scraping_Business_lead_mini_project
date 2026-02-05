from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from local_serpapi.client import SerpApiClient
from services.enricher import Enricher
from services.validator import Validator
from services.storage import Storage
import time

app = FastAPI()

@app.post("/scrape")
async def scrape(
    niche: str = Query(...,description="Business niche, e.g., Dentist, Restaurant"),
    location: str = Query(...,description="Location, e.g., Surat, Gujarat, India"),
    limit: int = Query(20,description="Number of results to return")
):
    serp = SerpApiClient()
    enricher = Enricher()
    validator = Validator()
    storage = Storage()

    try:
        candidates = serp.search(niche, location, limit)
    except Exception as e:
        print("SERP failed:", e)
        candidates = []

    enriched = []

    for c in candidates:
        try:
            e = enricher.enrich(c)
            if validator.validate(e):
                enriched.append(e)
            time.sleep(0.5)
        except:
            continue

    path = "output/business_details.csv"
    storage.save_to_csv(enriched, path)

    return JSONResponse({
        "saved": len(enriched),
        "file": path
    })
