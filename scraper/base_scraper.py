import requests
from bs4 import BeautifulSoup
import time, random

class BaseScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
            )
        }

    def get_page(self, url):
        """Fetch a page with a polite delay to avoid being blocked."""
        time.sleep(random.uniform(2, 4))
        response = requests.get(url, headers=self.headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")

    def extract_jobs(self, soup):
        raise NotImplementedError("Each scraper must implement extract_jobs()")