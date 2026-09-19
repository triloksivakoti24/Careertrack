CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    company TEXT NOT NULL CHECK (length(trim(company)) > 0),

    role TEXT NOT NULL CHECK (length(trim(role)) > 0),

    location TEXT,

    application_date TEXT NOT NULL,

    job_link TEXT,

    status TEXT NOT NULL DEFAULT 'Applied'
        CHECK (
            status IN (
                'Applied',
                'Interview',
                'Selected',
                'Rejected'
            )
        ),

    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX IF NOT EXISTS idx_applications_status
ON applications(status);


CREATE INDEX IF NOT EXISTS idx_applications_company
ON applications(company);


CREATE INDEX IF NOT EXISTS idx_applications_application_date
ON applications(application_date);


CREATE TRIGGER IF NOT EXISTS update_applications_updated_at
AFTER UPDATE ON applications
FOR EACH ROW
BEGIN
    UPDATE applications
    SET updated_at = CURRENT_TIMESTAMP
    WHERE id = OLD.id;
END;