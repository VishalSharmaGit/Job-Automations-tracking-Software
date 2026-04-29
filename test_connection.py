import pyodbc

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-K6PDKA3;"
    "DATABASE=master;"
    "Trusted_Connection=yes;"
)

try:
    conn = pyodbc.connect(conn_str)
    print("✅ Connected to SQL Server successfully!")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")