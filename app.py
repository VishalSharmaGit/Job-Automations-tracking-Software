# app.py  ← root folder
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import traceback
from flask import Flask, jsonify, request
from flask_cors import CORS
from database.db_connection import get_connection, rows_to_dict
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)

@app.route("/api/jobs", methods=["GET"])
def get_jobs():
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                j.id, j.title, j.company, j.location,
                j.skills, j.link, j.posted, j.source,
                j.scraped_at, j.is_relevant,
                COALESCE(a.status, 'Pending') AS status
            FROM jobs j
            LEFT JOIN applications a ON j.id = a.job_id
            ORDER BY j.scraped_at DESC
        """)
        jobs = rows_to_dict(cursor)
        conn.close()
        return jsonify(jobs)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/api/jobs/<int:job_id>/status", methods=["PATCH"])
def update_status(job_id):
    try:
        data   = request.get_json()
        status = data.get("status", "Pending")
        conn   = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM applications WHERE job_id = ?", (job_id,)
        )
        existing = cursor.fetchone()

        if existing:
            cursor.execute(
                "UPDATE applications SET status = ? WHERE job_id = ?",
                (status, job_id)
            )
        else:
            cursor.execute(
                "INSERT INTO applications (job_id, status) VALUES (?, ?)",
                (job_id, status)
            )

        conn.commit()
        conn.close()
        return jsonify({"message": "Status updated"})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)