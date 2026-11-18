-- ==========================================================
-- PROJECT: Hostel Occupancy and Attendance Analytics
-- FILE: 03_curfew_violations_and_repeat_offenders.sql
-- AUTHOR: Nithin K S (GitHub: NithinKs0405)
-- PURPOSE: Curfew late entries (>9:30 PM), night exits, and chronic repeat offender tracking
-- ==========================================================

-- 1. Curfew Violations by Hostel Block & Gender
SELECT 
    s.block_name,
    s.gender,
    COUNT(l.log_id) AS late_entry_count,
    COUNT(DISTINCT s.student_id) AS unique_late_students,
    ROUND(COUNT(l.log_id) * 1.0 / COUNT(DISTINCT s.student_id), 2) AS avg_violations_per_student
FROM attendance_logs l
JOIN students s ON l.student_id = s.student_id
WHERE l.is_curfew_late_entry = 1
GROUP BY s.block_name, s.gender
ORDER BY late_entry_count DESC;

-- 2. Top 15 Chronic Repeat Curfew Offenders (For Warden Review)
WITH offender_counts AS (
    SELECT 
        s.student_id,
        s.full_name,
        s.block_name,
        s.room_number,
        s.department,
        COUNT(l.log_id) AS late_count,
        MAX(l.timestamp) AS most_recent_violation,
        DENSE_RANK() OVER (ORDER BY COUNT(l.log_id) DESC) AS offender_rank
    FROM attendance_logs l
    JOIN students s ON l.student_id = s.student_id
    WHERE l.is_curfew_late_entry = 1
    GROUP BY s.student_id, s.full_name, s.block_name, s.room_number, s.department
)
SELECT * 
FROM offender_counts
WHERE offender_rank <= 15;

-- 3. High-Security Risk: Unauthorized Night Exits (Leaving between 10 PM and 5 AM)
SELECT 
    s.student_id,
    s.full_name,
    s.block_name,
    s.room_number,
    l.timestamp AS exit_timestamp,
    l.gate
FROM attendance_logs l
JOIN students s ON l.student_id = s.student_id
WHERE l.is_night_exit_anomaly = 1
ORDER BY l.timestamp DESC;
