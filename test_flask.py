# test_flask.py  — paste in root folder
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({"status": "working"})

@app.route("/api/jobs")
def jobs():
    return jsonify([
        {"id": 1, "title": "Data Analyst", "company": "TCS",
         "location": "Bangalore", "source": "Naukri",
         "posted": "2024-04-20", "link": "https://naukri.com", "status": "Pending"},
        {"id": 2, "title": "Senior Analyst", "company": "Infosys",
         "location": "Hyderabad", "source": "LinkedIn",
         "posted": "2024-04-21", "link": "https://linkedin.com", "status": "Pending"}
    ])

if __name__ == "__main__":
    app.run(debug=False, port=5000)