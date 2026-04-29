# scraper/naukri_scraper.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from datetime import datetime
from database.insert_jobs import insert_jobs

# ── Paste your RapidAPI key here ──────────────────────────
RAPIDAPI_KEY = "2425a1ad66mshe21564204dbf38ep1fbf51jsn922aa538d577"

class NaukriScraper:
    """
    Uses JSearch API (RapidAPI) to fetch real Data Analyst jobs
    from LinkedIn, Naukri, Indeed and 20+ job boards combined.
    Free plan: 500 requests/month
    """

    def __init__(self):
        self.url     = "https://jsearch.p.rapidapi.com/search"
        self.headers = {
            "X-RapidAPI-Key":  RAPIDAPI_KEY,
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }

    def scrape(self, pages=3):
        all_jobs = []
        for page in range(1, pages + 1):
            print(f"Fetching page {page}...")
            jobs = self.fetch_page(page)
            all_jobs.extend(jobs)
            print(f"  Found {len(jobs)} jobs on page {page}")
        print(f"\nTotal fetched: {len(all_jobs)} jobs")
        return all_jobs

    def fetch_page(self, page=1):
        params = {
            "query":           "Data Analyst India",
            "page":            str(page),
            "num_pages":       "1",
            "date_posted":     "week",       # only jobs from last 7 days
            "country":         "in",         # India
            "language":        "en"
        }
        try:
            response = requests.get(
                self.url,
                headers=self.headers,
                params=params,
                timeout=15
            )
            print(f"  Status: {response.status_code}")

            if response.status_code != 200:
                print(f"  ❌ Error: {response.text[:200]}")
                return []

            data = response.json()
            return self.parse_jobs(data)

        except Exception as e:
            print(f"  ❌ Exception: {e}")
            return []

    def parse_jobs(self, data):
        jobs     = []
        job_list = data.get("data", [])

        for job in job_list:
            try:
                # Extract skills from description
                description = job.get("job_description", "")
                skills      = self.extract_skills(description)

                jobs.append({
                    "title":      job.get("job_title",         "N/A"),
                    "company":    job.get("employer_name",     "N/A"),
                    "location":   f"{job.get('job_city', '')}, {job.get('job_country', '')}".strip(", "),
                    "skills":     skills,
                    "link":       job.get("job_apply_link",    "N/A"),
                    "posted":     job.get("job_posted_at_datetime_utc", datetime.now().isoformat())[:10],
                    "source":     job.get("job_publisher",     "JSearch"),
                    "scraped_at": datetime.now().isoformat()
                })
            except Exception as e:
                print(f"  Skipping job: {e}")
                continue

        return jobs

    def extract_skills(self, description):
        """Scan job description for known keywords."""
        known_skills = [
            "SQL", "Python", "Power BI", "Tableau", "Excel",
            "Pandas", "NumPy", "R", "Spark", "Hadoop",
            "Machine Learning", "Statistics", "ETL",
            "Data Visualization", "Looker", "DAX", "AWS", "Azure"
        ]
        found = [
            skill for skill in known_skills
            if skill.lower() in description.lower()
        ]
        return ", ".join(found) if found else "Not specified"


# ── Run directly to test ───────────────────────────────────
if __name__ == "__main__":
    scraper = NaukriScraper()
    jobs    = scraper.scrape(pages=1)

    print(f"\n{'='*50}")
    print(f"RESULTS: {len(jobs)} jobs found")
    print(f"{'='*50}")

    if jobs:
        print("\nSample job:")
        for key, val in jobs[0].items():
            print(f"  {key:12}: {val}")
        
        # Save jobs to database
        print("\n💾 Saving jobs to database...")
        inserted = insert_jobs(jobs)
        print(f"✅ Successfully saved {inserted} jobs to database!")
    else:
        print("No jobs returned. Check your API key.")