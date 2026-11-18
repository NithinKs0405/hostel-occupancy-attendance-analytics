-- ==========================================================
-- PROJECT: Hostel Occupancy and Attendance Analytics
-- FILE: 01_schema_hostel_db.sql
-- AUTHOR: Nithin K S (GitHub: NithinKs0405)
-- PURPOSE: Schema definitions for student residents and biometric RFID turnstiles
-- ==========================================================

CREATE TABLE IF NOT EXISTS students (
    student_id VARCHAR(20) PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    department VARCHAR(50) NOT NULL,
    year_of_study INT NOT NULL,
    block_name VARCHAR(50) NOT NULL,
    room_number VARCHAR(20) NOT NULL,
    curfew_time TIME DEFAULT '21:30:00'
);

CREATE TABLE IF NOT EXISTS attendance_logs (
    log_id VARCHAR(30) PRIMARY KEY,
    student_id VARCHAR(20) NOT NULL,
    timestamp DATETIME NOT NULL,
    direction VARCHAR(5) NOT NULL CHECK (direction IN ('IN', 'OUT')),
    gate VARCHAR(50) NOT NULL,
    device_status VARCHAR(20) DEFAULT 'Verified',
    date DATE NOT NULL,
    hour INT NOT NULL CHECK (hour BETWEEN 0 AND 23),
    day_of_week VARCHAR(15) NOT NULL,
    is_curfew_late_entry BOOLEAN NOT NULL DEFAULT 0,
    is_night_exit_anomaly BOOLEAN NOT NULL DEFAULT 0,
    CONSTRAINT fk_stud FOREIGN KEY (student_id) REFERENCES students(student_id)
);

CREATE INDEX idx_logs_timestamp ON attendance_logs(timestamp);
CREATE INDEX idx_logs_student ON attendance_logs(student_id);
CREATE INDEX idx_logs_date_direction ON attendance_logs(date, direction);
CREATE INDEX idx_students_block ON students(block_name);
