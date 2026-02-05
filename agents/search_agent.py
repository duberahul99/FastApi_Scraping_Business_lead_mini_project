# search_agent.py

"""
This script orchestrates SERP queries and enrichment. It accepts CLI inputs directly.
"""

import argparse
import sys
import os

# Ensure the parent directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from local_serpapi.client import SerpApiClient
from services.enricher import Enricher
from services.storage import Storage
from services.validator import Validator

def main():
    parser = argparse.ArgumentParser(description="Search Agent for extracting business details.")
    parser.add_argument("--niche", required=True, help="Business niche, e.g., Dentist, Restaurant")
    parser.add_argument("--location", required=True, help="Location, e.g., Surat, Gujarat, India")
    parser.add_argument("--limit", type=int, default=100, help="Maximum number of candidates to return")

    args = parser.parse_args()

    # Initialize components
    serp_client = SerpApiClient()
    enricher = Enricher()
    validator = Validator()
    storage = Storage()

    # Ensure output directory and CSV file exist
    output_dir = "output"
    csv_file_path = os.path.join(output_dir, "business_details.csv")
    os.makedirs(output_dir, exist_ok=True)

    # Ensure the CSV file exists with headers
    storage.ensure_csv_exists(csv_file_path)

    # Query SERP API
    candidates = serp_client.search(args.niche, args.location, args.limit)

    # Enrich and validate candidates
    enriched_candidates = []
    for candidate in candidates:
        enriched = enricher.enrich(candidate)
        if validator.validate(enriched):
            enriched_candidates.append(enriched)

    # Store results
    storage.save_to_csv(enriched_candidates, csv_file_path)

if __name__ == "__main__":
    main()