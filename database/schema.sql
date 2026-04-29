-- =============================================
-- Job Tracker Database Schema (SQL Server)
-- =============================================
SELECT DB_NAME() AS CurrentDB;
-- Create jobs table
IF NOT EXISTS (
    SELECT * FROM sysobjects 
    WHERE name = 'jobs' AND xtype = 'U'
)
BEGIN
    CREATE TABLE jobs (
        id          INT IDENTITY(1,1)  PRIMARY KEY,
        title       NVARCHAR(255)      NOT NULL,
        company     NVARCHAR(255)      NOT NULL,
        location    NVARCHAR(255)      NULL,
        skills      NVARCHAR(MAX)      NULL,
        link        NVARCHAR(MAX)      NOT NULL,
        posted      NVARCHAR(100)      NULL,
        source      NVARCHAR(50)       NULL,
        scraped_at  DATETIME2          DEFAULT GETDATE(),
        is_relevant BIT                DEFAULT 0
    );

    -- Unique constraint on link (prevents duplicate job entries)
    -- SQL Server cannot put UNIQUE directly on NVARCHAR(MAX),
    -- so we use a computed hash column as the unique key
    ALTER TABLE jobs
        ADD link_hash AS CONVERT(CHAR(64), HASHBYTES('SHA2_256', link), 2) PERSISTED;

    ALTER TABLE jobs
        ADD CONSTRAINT uq_jobs_link_hash UNIQUE (link_hash);

    PRINT 'Table [jobs] created successfully.';
END
ELSE
BEGIN
    PRINT 'Table [jobs] already exists. Skipping.';
END;
GO

-- =============================================
-- Create applications table
-- =============================================

IF NOT EXISTS (
    SELECT * FROM sysobjects 
    WHERE name = 'applications' AND xtype = 'U'
)
BEGIN
    CREATE TABLE applications (
        id          INT IDENTITY(1,1)  PRIMARY KEY,
        job_id      INT                NOT NULL,
        status      NVARCHAR(50)       DEFAULT 'Pending',   -- Applied / Pending / Rejected
        applied_at  DATETIME2          DEFAULT GETDATE(),
        notes       NVARCHAR(MAX)      NULL,

        CONSTRAINT fk_applications_job
            FOREIGN KEY (job_id) REFERENCES jobs(id)
            ON DELETE CASCADE,

        CONSTRAINT chk_status
            CHECK (status IN ('Pending', 'Applied', 'Rejected'))
    );

    PRINT 'Table [applications] created successfully.';
END
ELSE
BEGIN
    PRINT 'Table [applications] already exists. Skipping.';
END;
GO

-- =============================================
-- Create indexes (only if they don't exist)
-- =============================================

IF NOT EXISTS (
    SELECT * FROM sys.indexes 
    WHERE name = 'idx_jobs_company' AND object_id = OBJECT_ID('jobs')
)
BEGIN
    CREATE INDEX idx_jobs_company ON jobs(company);
    PRINT 'Index [idx_jobs_company] created.';
END;
GO

IF NOT EXISTS (
    SELECT * FROM sys.indexes 
    WHERE name = 'idx_jobs_location' AND object_id = OBJECT_ID('jobs')
)
BEGIN
    CREATE INDEX idx_jobs_location ON jobs(location);
    PRINT 'Index [idx_jobs_location] created.';
END;
GO

IF NOT EXISTS (
    SELECT * FROM sys.indexes 
    WHERE name = 'idx_jobs_posted' AND object_id = OBJECT_ID('jobs')
)
BEGIN
    CREATE INDEX idx_jobs_posted ON jobs(posted);
    PRINT 'Index [idx_jobs_posted] created.';
END;
GO

IF NOT EXISTS (
    SELECT * FROM sys.indexes 
    WHERE name = 'idx_jobs_source' AND object_id = OBJECT_ID('jobs')
)
BEGIN
    CREATE INDEX idx_jobs_source ON jobs(source);
    PRINT 'Index [idx_jobs_source] created.';
END;
GO

-- =============================================
-- Verify: view both tables
-- =============================================

SELECT 
    TABLE_NAME,
    COLUMN_NAME,
    DATA_TYPE,
    CHARACTER_MAXIMUM_LENGTH,
    IS_NULLABLE,
    COLUMN_DEFAULT
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME IN ('jobs', 'applications')
ORDER BY TABLE_NAME, ORDINAL_POSITION;
GO