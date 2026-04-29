CREATE DATABASE job_tracker;

-- Step 3: Switch to the new database
USE job_tracker;
GO

-- Step 4: Create jobs table
CREATE TABLE jobs (
    id          INT IDENTITY(1,1) PRIMARY KEY,
    title       NVARCHAR(255)     NOT NULL,
    company     NVARCHAR(255)     NOT NULL,
    location    NVARCHAR(255)     NULL,
    skills      NVARCHAR(MAX)     NULL,
    link        NVARCHAR(MAX)     NOT NULL,
    posted      NVARCHAR(100)     NULL,
    source      NVARCHAR(50)      NULL,
    scraped_at  DATETIME2         DEFAULT GETDATE(),
    is_relevant BIT               DEFAULT 0
);

-- Step 5: Add hash column for duplicate prevention
ALTER TABLE jobs
    ADD link_hash AS CONVERT(CHAR(64), HASHBYTES('SHA2_256', link), 2) PERSISTED;

ALTER TABLE jobs
    ADD CONSTRAINT uq_jobs_link_hash UNIQUE (link_hash);

-- Step 6: Create applications table
CREATE TABLE applications (
    id         INT IDENTITY(1,1) PRIMARY KEY,
    job_id     INT               NOT NULL,
    status     NVARCHAR(50)      DEFAULT 'Pending',
    applied_at DATETIME2         DEFAULT GETDATE(),
    notes      NVARCHAR(MAX)     NULL,
    CONSTRAINT fk_applications_job
        FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
    CONSTRAINT chk_status
        CHECK (status IN ('Pending', 'Applied', 'Rejected'))
);

-- Step 7: Create indexes
CREATE INDEX idx_jobs_company  ON jobs(company);
CREATE INDEX idx_jobs_location ON jobs(location);
CREATE INDEX idx_jobs_posted   ON jobs(posted);
CREATE INDEX idx_jobs_source   ON jobs(source);

PRINT 'All tables created successfully!';
GO

USE job_tracker;
GO

INSERT INTO jobs (title, company, location, skills, link, posted, source, is_relevant)
VALUES 
('Data Analyst',        'TCS',       'Bangalore', 'SQL, Python, Excel, Power BI',
 'https://naukri.com/job1', '2024-04-20', 'Naukri',   1),
('Senior Data Analyst', 'Infosys',   'Hyderabad', 'Power BI, SQL, Tableau',
 'https://naukri.com/job2', '2024-04-21', 'Naukri',   1),
('Junior Data Analyst', 'Wipro',     'Mumbai',    'Python, Pandas, Excel',
 'https://linkedin.com/job3','2024-04-22', 'LinkedIn', 1),
('Business Analyst',    'HCL',       'Pune',      'SQL, Excel, Jira',
 'https://linkedin.com/job4','2024-04-22', 'LinkedIn', 0),
('Data Analyst Intern', 'Accenture', 'Delhi',     'Python, SQL, Power BI',
 'https://naukri.com/job5', '2024-04-23', 'Naukri',   1);

-- Verify
SELECT * FROM jobs;
SELECT id, title, company, location FROM jobs;
GO