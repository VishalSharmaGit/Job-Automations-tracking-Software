# naukri_scraper.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper.base_scraper import BaseScraper   # ← remove the dot
from datetime import datetime

class NaukriScraper(BaseScraper):
    BASE_URL = "https://www.naukri.com/data-analyst-jobs-{page}"

    def scrape(self, pages=5):
        all_jobs = []
        for page in range(1, pages + 1):
            url = self.BASE_URL.format(page=page)
            print(f"Scraping page {page}: {url}")
            soup = self.get_page(url)
            jobs = self.extract_jobs(soup)
            all_jobs.extend(jobs)
        return all_jobs

    def extract_jobs(self, soup):
        jobs = []
        for card in soup.find_all("article", class_="jobTuple"):
            try:
                title    = card.find("a",    class_="title").text.strip()
                company  = card.find("a",    class_="subTitle").text.strip()
                location = card.find("li",   class_="location").text.strip()
                skills   = [s.text.strip() for s in card.find_all("li", class_="tag")]
                link     = card.find("a",    class_="title")["href"]
                posted   = card.find("span", class_="date").text.strip()

                jobs.append({
                    "title":      title,
                    "company":    company,
                    "location":   location,
                    "skills":     ", ".join(skills),
                    "link":       link,
                    "posted":     posted,
                    "source":     "Naukri",
                    "scraped_at": datetime.now().isoformat()
                })
            except AttributeError:
                continue
        return jobs