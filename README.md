# nc-water-quality-scrapper

A python web scraper that pulls water contamination data from the EWG Tap Water Database for cities across North Carolina

## What it does
- Scrapes contaminant names, levels, EWG health guidelines, and health effects of each chemical
- Exports structured data to CSV
- Covers 175 NC water utilities with 3,357 contaminant records
- Analyzes and answers questions including:
    - Most Contaminated Utilities
    - Most Extreme Violations of the EWG health guidelines
    - PFAS Contamination
    - Fayetteville Spotlight Rank
    - Cleanest Utilities
    - Most Widespread Contaminants

## Built with
- Python
- BeautifulSoup4
- Requests
