# Business Details Extraction

This project implements a SERP-first workflow to extract business details for a given niche and location using the SERP API. The extracted data is saved as a structured CSV file.

## Features
- Query SERP API for business details
- Enrich data with social media links
- Validate and normalize data
- Save results to CSV

## Project Structure
- `agents/`: CLI entrypoints for automation
- `serpapi/`: SERP API integration
- `services/`: Data enrichment, validation, and storage
- `data/`: Intermediate datasets
- `output/`: Final output files
- `tests/`: Unit tests

## Quick Start
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the search agent:
   ```bash
   python agents/search_agent.py --niche "Dentist" --location "Surat, Gujarat, India" --limit 100
   ```
3. Check the output in `output/business_details.csv`.

## Requirements
- Python 3.8+
- SERP API key