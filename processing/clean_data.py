# processing/clean_data.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from database.db_connection import get_connection

RELEVANT_KEYWORDS = ["sql", "python", "power bi", "tableau", "excel", "data analyst"]

def load_jobs():
    conn = get_connection()
    df   = pd.read_sql("SELECT * FROM jobs", conn)
    conn.close()
    return df

def is_relevant(row):
    text = f"{row['title']} {row.get('skills', '')}".lower()
    return any(kw in text for kw in RELEVANT_KEYWORDS)

def clean_and_tag():
    df = load_jobs()

    if df.empty:
        print("No jobs found in database.")
        return df

    # Clean whitespace
    df["title"]    = df["title"].str.strip().str.title()
    df["company"]  = df["company"].str.strip().str.title()
    df["location"] = df["location"].fillna("").str.strip()
    df["skills"]   = df["skills"].fillna("")

    # Remove rows with no title or link
    df = df.dropna(subset=["title", "link"])
    df = df.drop_duplicates(subset=["link"])

    # Tag relevance
    df["is_relevant"] = df.apply(is_relevant, axis=1)

    # Write tags back — use ? placeholder for SQL Server
    conn   = get_connection()
    cursor = conn.cursor()
    for _, row in df.iterrows():
        cursor.execute(
            "UPDATE jobs SET is_relevant = ? WHERE id = ?",
            (1 if row["is_relevant"] else 0, int(row["id"]))
        )
    conn.commit()
    cursor.close()
    conn.close()

    print(f"✅ Tagged {df['is_relevant'].sum()} relevant jobs out of {len(df)}.")
    return df[df["is_relevant"]]