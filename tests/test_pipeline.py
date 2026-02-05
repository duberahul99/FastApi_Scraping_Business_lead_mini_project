# test_pipeline.py

"""
Unit tests for the pipeline.
"""

import sys
import os
import unittest
from local_serpapi.client import SerpApiClient
from services.enricher import Enricher
from services.validator import Validator
from services.storage import Storage

# Ensure the project root is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestPipeline(unittest.TestCase):
    def test_pipeline(self):
        serp_client = SerpApiClient(api_key="test_key")
        enricher = Enricher()
        validator = Validator()
        storage = Storage()

        # Mock data
        candidates = [
            {"name": "Test Business", "address": "123 Test St", "phone": "123-456-7890"}
        ]

        enriched_candidates = []
        for candidate in candidates:
            enriched = enricher.enrich(candidate)
            if validator.validate(enriched):
                enriched_candidates.append(enriched)

        self.assertEqual(len(enriched_candidates), 1)
        self.assertEqual(enriched_candidates[0]["name"], "Test Business")

if __name__ == "__main__":
    unittest.main()


