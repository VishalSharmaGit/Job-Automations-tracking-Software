# 🚀 Job Automation & Tracking System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQL Server](https://img.shields.io/badge/SQL%20Server-CC2927?style=for-the-badge&logo=microsoftsqlserver&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)

**An end-to-end automated pipeline that fetches, stores, processes and displays real-time Data Analyst job listings — fully automated, zero manual effort.**

[Features](#-features) • [Architecture](#-architecture) • [Tech Stack](#-tech-stack) • [Setup](#-setup--installation) • [Usage](#-usage) • [Dashboard](#-dashboard-preview) • [Folder Structure](#-folder-structure)

</div>

---

## 📌 About The Project

As a Data Analyst aspirant, manually checking Naukri and LinkedIn for new jobs every day is time-consuming and inefficient.

This project **automates the entire job search workflow**:
- Fetches real-time Data Analyst job listings via **JSearch API** (pulls from LinkedIn, Naukri, Indeed & 20+ boards)
- Stores and deduplicates data in a structured **SQL Server** database
- Displays everything on an interactive **HTML + JavaScript dashboard**
- Sends **email alerts** for new relevant jobs
- Runs **automatically every day** via Windows Task Scheduler

> 💡 Built as a real portfolio-level project to showcase end-to-end data engineering, backend development, and automation skills.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **Automated Job Fetching** | Pulls 50+ fresh Data Analyst jobs daily via REST API |
| 🗄️ **SQL Server Storage** | Normalized schema with indexing and duplicate prevention |
| 🧹 **Data Processing** | Cleans and filters jobs by keywords (SQL, Python, Power BI) |
| 📊 **Interactive Dashboard** | Filter by location, source, status — live in browser |
| 📧 **Email Alerts** | Auto-sends digest of top relevant jobs to your inbox |
| 🔄 **Status Tracking** | Track each job as Pending / Applied / Rejected |
| ⏰ **Daily Automation** | Runs fully automatically via Windows Task Scheduler |
| 🐍 **Flask REST API** | Python backend serves data to the frontend dashboard |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA COLLECTION                          │
│         JSearch API (LinkedIn + Naukri + Indeed)            │
│              Python → requests + pandas                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATA STORAGE                             │
│              SQL Server (job_tracker DB)                    │
│       jobs table + applications table + indexes             │
│         Deduplication via SHA-256 hash constraint           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   DATA PROCESSING                           │
│           Python + pandas → clean_data.py                   │
│     Keyword filtering · Relevance tagging · Deduplication   │
└──────────┬──────────────────────────────────┬───────────────┘
           │                                  │
           ▼                                  ▼
┌─────────────────────┐            ┌─────────────────────────┐
│   FLASK REST API    │            │   EMAIL NOTIFICATIONS   │
│   app.py → :5000    │            │  smtplib → Gmail SMTP   │
│  /api/jobs endpoint │            │  Top 10 relevant jobs   │
└─────────┬───────────┘            └─────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│                  HTML/JS DASHBOARD                          │
│          index.html + app.js → Live Server :5500            │
│    Filter by location · source · status · search bar        │
│         Status dropdown: Pending → Applied → Rejected       │
└─────────────────────────────────────────────────────────────┘
          ▲
          │
┌─────────────────────────────────────────────────────────────┐
│                     AUTOMATION                              │
│         Windows Task Scheduler → runs daily at 8 AM        │
│      scheduler.py → scrape → store → process → notify       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Data Collection** | Python, JSearch API (RapidAPI) | Fetch real-time job listings |
| **Data Storage** | SQL Server, pyodbc | Store and query job data |
| **Data Processing** | Python, pandas | Clean, filter, tag relevant jobs |
| **Backend API** | Flask, flask-cors | Serve job data to dashboard |
| **Frontend** | HTML, CSS, JavaScript | Interactive job dashboard |
| **Notifications** | Python smtplib, Gmail SMTP | Email alerts for new jobs |
| **Automation** | Windows Task Scheduler | Daily pipeline execution |

---

## 📁 Folder Structure

```
Job Automation & Tracking System/
│
├── app.py                        # Flask REST API (main backend)
├── test_connection.py            # SQL Server connection test
├── test_flask.py                 # Flask server test
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables (not committed)
│
├── scraper/
│   ├── __init__.py
│   ├── base_scraper.py           # Base class with shared HTTP logic
│   ├── naukri_scraper.py         # JSearch API scraper (main)
│   └── linkedin_scraper.py       # Selenium scraper (optional)
│
├── database/
│   ├── __init__.py
│   ├── db_connection.py          # SQL Server connection manager
│   ├── insert_jobs.py            # Insert + deduplicate job records
│   └── schema.sql                # Full database schema
│
├── processing/
│   ├── __init__.py
│   └── clean_data.py             # Clean, filter, tag relevant jobs
│
├── notifications/
│   ├── __init__.py
│   └── email_alert.py            # Gmail SMTP email alerts
│
├── automation/
│   ├── __init__.py
│   └── scheduler.py              # Full pipeline runner
│
└── dashboard/
    ├── index.html                # Job tracker UI
    └── app.js                    # Fetch API + filter + status logic
```

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.10+
- SQL Server (or SQL Server Express)
- ODBC Driver 17 for SQL Server
- Google Chrome (for Selenium, optional)
- RapidAPI account (free) for JSearch API

---

### Step 1 — Clone the repository

```bash
git clone https://github.com/yourusername/job-automation-tracking-system.git
cd job-automation-tracking-system
```

### Step 2 — Create virtual environment

```bash
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Create `.env` file in root folder

```env
DB_SERVER=YOUR_SERVER_NAME
DB_DATABASE=job_tracker
DB_TRUSTED_CONNECTION=yes
RAPIDAPI_KEY=your_rapidapi_key_here
```

> Get your free RapidAPI key at → https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch

### Step 5 — Set up SQL Server database

Open **SQL Server Management Studio (SSMS)** and run `database/schema.sql`:

```sql
-- Creates job_tracker database, jobs table, applications table, and all indexes
```

### Step 6 — Test database connection

```bash
python test_connection.py
# Expected: ✅ Connected to SQL Server successfully!
```

### Step 7 — Insert sample data (optional, for testing)

```sql
USE job_tracker;
INSERT INTO jobs (title, company, location, skills, link, posted, source, is_relevant)
VALUES
('Data Analyst', 'TCS', 'Bangalore', 'SQL, Python, Power BI', 'https://naukri.com/job1', '2024-04-20', 'Naukri', 1),
('Senior Data Analyst', 'Infosys', 'Hyderabad', 'Tableau, SQL', 'https://naukri.com/job2', '2024-04-21', 'Naukri', 1);
```

---

## 🚀 Usage

### Run the full pipeline manually

```bash
python automation/scheduler.py
```

### Start just the Flask API

```bash
python app.py
# API runs at → http://127.0.0.1:5000/api/jobs
```

### Open the dashboard

In VS Code → right-click `dashboard/index.html` → **Open with Live Server**

Dashboard opens at → `http://127.0.0.1:5500/dashboard/index.html`

### Run only the scraper

```bash
python scraper/naukri_scraper.py
```

### Run only data processing

```bash
python processing/clean_data.py
```

---

## 🗄️ Database Schema

```sql
-- jobs table
CREATE TABLE jobs (
    id          INT IDENTITY(1,1) PRIMARY KEY,
    title       NVARCHAR(255)     NOT NULL,
    company     NVARCHAR(255)     NOT NULL,
    location    NVARCHAR(255),
    skills      NVARCHAR(MAX),
    link        NVARCHAR(MAX)     NOT NULL,
    posted      NVARCHAR(100),
    source      NVARCHAR(50),
    scraped_at  DATETIME2         DEFAULT GETDATE(),
    is_relevant BIT               DEFAULT 0,
    link_hash   AS CONVERT(CHAR(64), HASHBYTES('SHA2_256', link), 2) PERSISTED,
    CONSTRAINT uq_jobs_link_hash UNIQUE (link_hash)
);

-- applications table
CREATE TABLE applications (
    id         INT IDENTITY(1,1) PRIMARY KEY,
    job_id     INT REFERENCES jobs(id) ON DELETE CASCADE,
    status     NVARCHAR(50) DEFAULT 'Pending'
               CHECK (status IN ('Pending', 'Applied', 'Rejected')),
    applied_at DATETIME2 DEFAULT GETDATE(),
    notes      NVARCHAR(MAX)
);
```

---

## 📊 Dashboard Preview

The dashboard provides:

- 🔍 **Search bar** — filter by job title or company name
- 📍 **Location filter** — filter by city
- 🌐 **Source filter** — LinkedIn / Naukri / Indeed
- 📋 **Status dropdown** — Pending / Applied / Rejected per job
- 🔗 **Direct apply links** — one click to apply

---

## 📧 Email Notifications Setup

1. Enable **2-Step Verification** on your Google account
2. Go to **Google Account → Security → App Passwords**
3. Generate a password for "Mail"
4. Update `notifications/email_alert.py`:

```python
FROM_EMAIL   = "your_email@gmail.com"
APP_PASSWORD = "xxxx xxxx xxxx xxxx"   # 16-character App Password
TO_EMAIL     = "your_email@gmail.com"
```

---

## ⏰ Automation Setup (Windows Task Scheduler)

```
1. Open Task Scheduler → Create Basic Task
2. Name: "Job Tracker Daily Run"
3. Trigger: Daily → 8:00 AM
4. Action: Start a Program
5. Program: C:\path\to\venv\Scripts\python.exe
6. Arguments: automation\scheduler.py
7. Start in: C:\path\to\project\root
8. Click Finish
```

---

## 📦 Requirements

```
requests==2.31.0
beautifulsoup4==4.12.2
selenium==4.15.0
pandas==2.1.1
Flask==3.0.0
flask-cors==4.0.0
pyodbc==5.0.1
python-dotenv==1.0.0
SQLAlchemy==2.0.23
```

Install all at once:
```bash
pip install -r requirements.txt
```

---

## 🔮 Future Improvements

- [ ] Power BI dashboard connected to SQL Server
- [ ] Looker Studio integration for trend visualisation
- [ ] LinkedIn scraper with Selenium
- [ ] Resume match scoring using NLP
- [ ] Google Sheets integration via Apps Script
- [ ] Docker containerization
- [ ] Deploy Flask API to cloud (AWS / Azure)

---

## 📄 Resume Description

> **Job Automation & Tracking System** | Python · SQL Server · Flask · JavaScript
>
> Built an end-to-end automated pipeline that fetches 50+ daily Data Analyst job listings via JSearch REST API. Designed a normalised SQL Server schema with SHA-256 hash-based unique constraints to eliminate duplicates. Implemented keyword-based relevance tagging in Python/pandas and scheduled daily execution via Windows Task Scheduler. Developed a Flask REST API serving data to an interactive HTML/JS dashboard with role, location and status filters. Automated email digests deliver curated job alerts with direct apply links via Gmail SMTP.

---

## 🤝 Connect With Me

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/yourprofile)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/yourusername)

---

## ⭐ If this project helped you, please give it a star!

```
git clone → setup → run → track jobs automatically 🎯
```

---

<div align="center">
Made with ❤️ by Vishal Sharma | Data Analyst
</div>
