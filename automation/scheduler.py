# automation/scheduler.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper.naukri_scraper       import NaukriScraper
from scraper.linkedin_scraper     import LinkedInScraper
from database.insert_jobs         import insert_jobs
from processing.clean_data        import clean_and_tag
from notifications.email_alert    import send_email_alert

def run():
    print("=== Job Tracker — Daily Run ===")

    # 1. Scrape
    print("Scraping Naukri...")
    naukri_jobs = NaukriScraper().scrape(pages=2)

    print("Scraping LinkedIn...")
    linkedin_jobs = LinkedInScraper().scrape(pages=2)

    all_jobs = naukri_jobs + linkedin_jobs
    print(f"Total scraped: {len(all_jobs)} raw listings.")

    # 2. Store
    new_count = insert_jobs(all_jobs)

    # 3. Process
    relevant_df = clean_and_tag()

    # 4. Notify
    if new_count > 0 and not relevant_df.empty:
        send_email_alert(relevant_df.head(10))
    else:
        print("No new relevant jobs to notify about.")

    print("=== Done ===")

if __name__ == "__main__":
    run()