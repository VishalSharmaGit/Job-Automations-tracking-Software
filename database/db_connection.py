import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "server":             os.environ.get("DB_SERVER",             "DESKTOP-K6PDKA3"),
    "database":           os.environ.get("DB_DATABASE",           "job_tracker"),
    "username":           os.environ.get("DB_USERNAME",           ""),
    "password":           os.environ.get("DB_PASSWORD",           ""),
    "trusted_connection": os.environ.get("DB_TRUSTED_CONNECTION", "yes").lower()
                          in ("yes", "true", "1"),
}

def get_connection():
    if DB_CONFIG["trusted_connection"]:
        conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            f"SERVER={DB_CONFIG['server']};"
            f"DATABASE={DB_CONFIG['database']};"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
    else:
        conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            f"SERVER={DB_CONFIG['server']};"
            f"DATABASE={DB_CONFIG['database']};"
            f"UID={DB_CONFIG['username']};"
            f"PWD={DB_CONFIG['password']};"
            "TrustServerCertificate=yes;"
        )
    return pyodbc.connect(conn_str)

def rows_to_dict(cursor):
    """Converts pyodbc rows → list of dicts (like psycopg2 RealDictCursor)."""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]