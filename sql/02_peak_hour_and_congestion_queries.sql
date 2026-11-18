-- ==========================================================
-- PROJECT: Hostel Occupancy and Attendance Analytics
-- FILE: 02_peak_hour_and_congestion_queries.sql
-- AUTHOR: Nithin K S (GitHub: NithinKs0405)
-- PURPOSE: Ingress/Egress hourly volume & gate congestion analysis
-- ==========================================================

-- 1. Hourly Traffic Distribution (Ingress vs. Egress)
SELECT 
    hour,
    SUM(CASE WHEN direction = 'OUT' THEN 1 ELSE 0 END) AS total_exits,
    SUM(CASE WHEN direction = 'IN' THEN 1 ELSE 0 END) AS total_entries,
    COUNT(*) AS total_turnstile_scans,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM attendance_logs), 2) AS traffic_percentage
FROM attendance_logs
GROUP BY hour
ORDER BY total_turnstile_scans DESC;

-- 2. Peak Gate Congestion Analysis by Hostel Block
SELECT 
    s.block_name,
    l.gate,
    l.hour,
    COUNT(*) AS scan_volume,
    RANK() OVER (PARTITION BY s.block_name ORDER BY COUNT(*) DESC) AS peak_rank
FROM attendance_logs l
JOIN students s ON l.student_id = s.student_id
WHERE l.hour IN (8, 17, 18) -- Peak morning egress (8 AM) and evening return (5-6 PM)
GROUP BY s.block_name, l.gate, l.hour
ORDER BY s.block_name, scan_volume DESC;
