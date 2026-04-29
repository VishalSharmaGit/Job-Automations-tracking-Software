from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

class LinkedInScraper:
    BASE_URL = (
        "https://www.linkedin.com/jobs/search/"
        "?keywords=Data+Analyst&location=India&start={start}"
    )

    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)

    def scrape(self, pages=5):
        all_jobs = []
        for page in range(pages):
            url = self.BASE_URL.format(start=page * 25)
            self.driver.get(url)
            # Wait for job cards to appear
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "job-search-card"))
            )
            time.sleep(2)
            cards = self.driver.find_elements(By.CLASS_NAME, "job-search-card")
            for card in cards:
                try:
                    all_jobs.append({
                        "title":      card.find_element(By.CLASS_NAME, "base-search-card__title").text,
                        "company":    card.find_element(By.CLASS_NAME, "base-search-card__subtitle").text,
                        "location":   card.find_element(By.CLASS_NAME, "job-search-card__location").text,
                        "skills":     "",           # enriched later in processing layer
                        "link":       card.find_element(By.TAG_NAME, "a").get_attribute("href"),
                        "posted":     card.find_element(By.TAG_NAME, "time").get_attribute("datetime"),
                        "source":     "LinkedIn",
                        "scraped_at": datetime.now().isoformat()
                    })
                except Exception:
                    continue
        self.driver.quit()
        return all_jobs