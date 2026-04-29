# database/insert_jobs.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_connection import get_connection

def insert_jobs(jobs: list):
    conn     = get_connection()
    cursor   = conn.cursor()
    inserted = 0

    for job in jobs:
        try:
            # Check if this link already exists (replaces ON CONFLICT)
            cursor.execute(
                "SELECT COUNT(*) FROM jobs WHERE link_hash = "
                "CONVERT(CHAR(64), HASHBYTES('SHA2_256', ?), 2)",
                (job.get("link", ""),)
            )
            exists = cursor.fetchone()[0]

            if not exists:
                cursor.execute("""
                    INSERT INTO jobs
                        (title, company, location, skills, link, posted, source)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    job.get("title",    ""),
                    job.get("company",  ""),
                    job.get("location", ""),
                    job.get("skills",   ""),
                    job.get("link",     ""),
                    job.get("posted",   ""),
                    job.get("source",   ""),
                ))
                inserted += 1

        except Exception as e:
            print(f"Error inserting job '{job.get('title')}': {e}")
            conn.rollback()
            continue

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Inserted {inserted} new jobs.")
    return inserted