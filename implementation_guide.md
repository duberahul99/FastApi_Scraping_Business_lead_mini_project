# IMPLEMENTATION GUIDE

## Overview ✅
**Purpose:** Implement a SERP-first workflow using FastAPI and the Google SERP API to reliably extract business details for a given niche and location. The primary geographic focus is **Surat, Gujarat, India**, but the process is generic.

**Primary Output:** structured CSV at `output/business_details.csv` with the following fields:
- Business Name
- Address
- Owner Name
- Phone Number
- Website Link
- Facebook Link
- Instagram Link
- LinkedIn Link
- Rating

---

## Inputs
- `niche` (string): e.g., "Dentist", "Restaurant"
- `location` (string): e.g., "Surat, Gujarat, India"
- `limit` (int, optional): maximum number of candidates to return (default: 100). Set a positive integer to limit results per run.
- Input method: Provide inputs via FastAPI endpoints.

---

## Key Principles 💡
- Use the Google SERP API to get structured SERP and Maps/local-pack results as JSON whenever possible.
- Follow the strict source order: **SERP API → Official website → Social media** (Facebook, Instagram, LinkedIn) for enrichment and corroboration. Only use third-party directories or public endpoints if they explicitly permit automated access and provide unique value. Avoid "pain APIs" or endpoints that prohibit scraping.
- Avoid direct HTML parsing with BS4 or browser automation (Selenium/Playwright) unless absolutely necessary and approved.
- Maintain strict validation, error handling, and logging for auditability.
- Respect site terms, robots.txt, and rate limits.

---

## High-Level Workflow
1. FastAPI Endpoint
   - Accepts `niche`, `location`, and `limit` as query parameters.
   - Returns JSON response with enriched business details.
2. Query construction
   - Primary query: `"<niche> in <location>"` and variants (e.g., "<niche> near <location>"):
     - Use SERP API parameters to request local-pack/Maps, knowledge panel, and organic results.
     - If `niche` is "all", retry with broader queries like `"businesses in <location>"` or `"<location> all"`.
3. Candidate extraction
   - Read the SERP API JSON and extract candidates from local pack entries, knowledge panels, and top organic directories. Honor the `limit` input by stopping after the requested number of unique candidates (default 100); support pagination and sub-queries as needed.
   - For each candidate, capture: name, address, phone (if returned), website URL, rating, social links (if provided), and raw source objects. Keep evidence URLs in `data/site_extractions.json` (not in the CSV).
4. Deep enrichment
   - When fields are missing, run targeted SERP API sub-queries (e.g., "<Business Name> <location> Facebook", "<Business Name> <location> Instagram", "<Business Name> phone").
   - Prefer SERP API JSON responses over raw HTML where possible.
5. Validation & normalization
   - Validate phone numbers (E.164 / national formats) and addresses (simple structural checks), normalize website URLs, and check social links are valid domains.
   - Validate Owner Name by finding it in official site snippets, GMB descriptions, or corroborating directory/social profiles.
6. Evidence & internal scoring
   - Keep full evidence (source types and corroborating URLs) and timestamps in `data/site_extractions.json`. Do **not** include a `Confidence` column in the CSV output; if internal scoring is used, keep it internal in logs and only use it for filtering/prioritization.
7. Output
   - Append validated rows to `output/business_details.csv`. Keep evidence and source URLs in `data/site_extractions.json` (the CSV should include only the output fields listed earlier).

---

## Validation & Error Handling 🔧
- Use typed data models (Pydantic) to enforce schema.
- Retries: exponential backoff (e.g., 1s, 2s, 4s) on transient failures; cap retries.
- Rate limits: throttle SERP API requests as per account limits; implement a token-bucket or simple sleep-based mechanism.
- Partial data handling: allow partial records; mark missing fields in `data/site_extractions.json`. Only include records in `output/business_details.csv` when they meet required field criteria (Business Name plus at least one of Address or Phone Number).
- Logging: record query, HTTP status, response ID, extraction result, and traceable evidence URLs.
- Exceptions: catch and surface API errors, JSON decode errors, and validation errors to an operations log (with timestamps).

---

## Data Schema (example)
- business_name: string
- address: string
- owner_name: string | null
- phone_number: string | null
- website: string | null
- facebook: string | null
- instagram: string | null
- rating: float | null
- sources: list[string]
- extracted_at: ISO8601 timestamp

---

## Workspace / File Layout (recommended) 📁
Root (relative to workspace):
- `agents/` — automation agents and CLI entrypoints
  - `agents/README.md` — agent conventions and ownership
  - `agents/search_agent.py` — orchestrates SERP queries and enrichment; accepts CLI inputs directly
- `serpapi/` — SERP integration layer (API clients and query builders)
  - `serpapi/client.py` — low-level SERP API calls, pagination, rate-limit handling
  - `serpapi/models.py` — response schemas and typed models
- `services/` — enrichment, validation, persistence
  - `services/enricher.py` — enforcement of source order: official site and social enrichers
  - `services/validator.py` — normalization and data validation (phone/address)
  - `services/storage.py` — CSV/JSON output writers and intermediate storage
- `data/` — saved intermediate datasets
  - `data/candidates.csv`
  - `data/site_extractions.json`
- `output/`
  - `output/business_details.csv` — final dataset
- `tests/` — unit/integration tests (mock SERP responses)
- `requirements.txt` — minimal deps (FastAPI, Pydantic, Requests)

---

## Implementation notes & sample flow 🔁
- Build `serpapi/client.py` to call the SERP API and return typed JSON.
- Implement FastAPI endpoints to accept inputs, issue queries, collect candidate lists, run enrichment, validate, and return JSON responses.
- Tests: add unit tests that mock SERP API responses and assert field extraction, validation, and JSON response structure.

---

## Compliance & Ethics ⚖️
- Only use public data; obey terms of service for each provider.
- Do not attempt to access private or authenticated pages.
- Rate-limit and respect robots.txt and provider policies.

---

## Quick Start (example commands)
```bash
# Create virtual env and install deps
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run FastAPI server
uvicorn app:app --reload

# Access the API at http://127.0.0.1:8000/docs
```

---

*Last updated:* 2026-02-04
