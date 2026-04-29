import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from scraper.naukri_scraper import NaukriScraper

scraper = NaukriScraper()
jobs = scraper.scrape(pages=1)

print(f"Total jobs scraped: {len(jobs)}")

# Print first 2 jobs
for job in jobs[:2]:
    print(job)