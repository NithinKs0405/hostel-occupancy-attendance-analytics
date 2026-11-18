-- ==========================================================
-- PROJECT: Hostel Occupancy and Attendance Analytics
-- FILE: 04_daily_occupancy_rates.sql
-- AUTHOR: Nithin K S (GitHub: NithinKs0405)
-- PURPOSE: Day-by-day attendance rate, occupancy trends, weekday vs weekend drop
-- ==========================================================

-- 1. Daily In-Hostel Attendance Percentage
WITH daily_stats AS (
    SELECT 
        l.date,
        l.day_of_week,
        COUNT(DISTINCT l.student_id) AS present_student_count,
        (SELECT COUNT(*) FROM students) AS total_enrolled_capacity
    FROM attendance_logs l
    WHERE l.direction = 'IN'
    GROUP BY l.date, l.day_of_week
)
SELECT 
    date,
    day_of_week,
    present_student_count,
    total_enrolled_capacity,
    ROUND((present_student_count * 100.0 / total_enrolled_capacity), 2) AS attendance_rate_pct,
    CASE 
        WHEN day_of_week IN ('Saturday', 'Sunday') THEN 'Weekend'
        ELSE 'Weekday'
    END AS day_type
FROM daily_stats
ORDER BY date ASC;

-- 2. Average Attendance Rate Comparison: Weekdays vs. Weekends
WITH daily_stats AS (
    SELECT 
        l.date,
        l.day_of_week,
        COUNT(DISTINCT l.student_id) AS present_student_count,
        (SELECT COUNT(*) FROM students) AS total_capacity
    FROM attendance_logs l
    WHERE l.direction = 'IN'
    GROUP BY l.date, l.day_of_week
)
SELECT 
    CASE WHEN day_of_week IN ('Saturday', 'Sunday') THEN 'Weekend Outings' ELSE 'Standard Weekday' END AS day_category,
    ROUND(AVG(present_student_count), 1) AS avg_students_present,
    ROUND(AVG(present_student_count * 100.0 / total_capacity), 2) AS avg_occupancy_rate_pct
FROM daily_stats
GROUP BY CASE WHEN day_of_week IN ('Saturday', 'Sunday') THEN 'Weekend Outings' ELSE 'Standard Weekday' END;
