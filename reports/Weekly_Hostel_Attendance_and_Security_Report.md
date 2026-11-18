# Hostel Occupancy & Attendance Surveillance Report

**Author:** Nithin K S  
**Role:** Data Analyst  
**Tools Employed:** Python (Pandas, NumPy, Matplotlib, Seaborn), SQL (SQLite/PostgreSQL), Power BI DAX  
**Dataset Analyzed:** 45,777 Biometric RFID Turnstile Events Across 450 Residents (60 Days)  

---

## 1. Executive Summary
An analytics audit was performed on turnstile telemetry and RFID attendance logs for **450 hostel residents** across Blocks A, B, C, and D over a 60-day period.

Key operational findings:
- **Peak Egress:** 07:30 to 08:45 AM (58% of all exits occur in this 75-minute window for academic lectures).
- **Peak Ingress:** 17:00 to 18:30 PM (62% of all daily returns).
- **Curfew Violations:** **983 instances** of entry past the 21:30 (9:30 PM) curfew deadline.
- **Unauthorized Night Exits:** **193 movements** between 22:00 and 05:00 AM requiring security review.
- **Attendance Rate:** Weekday average in-hostel occupancy is **91.4%**, which drops to **61.2% on weekends** due to authorized out-of-campus home visits.

---

## 2. Key Actionable Recommendations for Campus Administration
1. **Dynamic Gate Staffing at Turnstiles:** Deploy security marshals at Gate A and Gate C during 07:45–08:30 AM to prevent bottlenecks and student congestion.
2. **Automated SMS Curfew Alerts:** Trigger automated notifications to wardens and parents when an entry is recorded after 21:30 PM.
3. **Chronic Offender Counseling:** 18 students accounted for over 35% of all curfew infractions. Implement counseling and academic review for repeat offenders.
