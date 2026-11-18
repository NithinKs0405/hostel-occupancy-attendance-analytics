import os
import random
import sqlite3
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

def generate_hostel_system_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, 'data', 'raw')
    proc_dir = os.path.join(base_dir, 'data', 'processed')
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(proc_dir, exist_ok=True)
    
    print("Generating student residents master dataset...")
    blocks = {
        'Block A': ('Male', 120),
        'Block B': ('Male', 110),
        'Block C': ('Female', 110),
        'Block D': ('Female', 110)
    }
    
    first_names_male = ['Aarav', 'Vivaan', 'Aditya', 'Vihaan', 'Arjun', 'Sai', 'Reyansh', 'Ayaan', 'Krishna', 'Ishaan',
                        'Shaurya', 'Atharv', 'Rudra', 'Nithin', 'Kabir', 'Rishi', 'Karan', 'Dev', 'Manish', 'Sanjay']
    first_names_female = ['Saanvi', 'Aanya', 'Aadhya', 'Aaradhya', 'Ananya', 'Pari', 'Diya', 'Anika', 'Riya', 'Avni',
                          'Isha', 'Meera', 'Sneha', 'Pooja', 'Kavya', 'Priyanka', 'Raashmi', 'Deepika', 'Divya', 'Neha']
    last_names = ['Sharma', 'Verma', 'Patel', 'Reddy', 'Nair', 'Iyer', 'Kumar', 'Singh', 'Rao', 'Pillai',
                  'Gupta', 'Menon', 'Joshi', 'Bhat', 'Deshmukh', 'Kulkarni', 'Hegde', 'Chatterjee', 'Das', 'Sundaram']
    
    departments = ['Computer Science', 'AI & Data Science', 'Information Tech', 'Electronics', 'Mechanical']
    
    students = []
    stud_counter = 101
    for b_name, (b_gender, b_cap) in blocks.items():
        for i in range(1, b_cap + 1):
            s_id = f"STU-{stud_counter:04d}"
            fn = random.choice(first_names_male if b_gender == 'Male' else first_names_female)
            ln = random.choice(last_names)
            room = f"{b_name[6]}-{100 + (i % 30) + 10 * (i // 30)}"
            dept = random.choice(departments)
            yr = random.choices([1, 2, 3, 4], weights=[0.28, 0.26, 0.24, 0.22])[0]
            
            # Tendency for late entry (some students are chronic latecomers)
            late_propensity = random.choices([0.02, 0.08, 0.25], weights=[0.75, 0.20, 0.05])[0]
            
            students.append({
                'StudentID': s_id,
                'FullName': f"{fn} {ln}",
                'Gender': b_gender,
                'Department': dept,
                'YearOfStudy': yr,
                'BlockName': b_name,
                'RoomNumber': room,
                'CurfewTime': '21:30:00',
                'LatePropensity': late_propensity
            })
            stud_counter += 1
            
    df_students = pd.DataFrame(students)
    df_students.to_csv(os.path.join(raw_dir, 'students_master.csv'), index=False)
    print(f"Generated {len(df_students)} student resident records.")
    
    # Generate 60 days of turnstile logs (e.g. Sept 1, 2026 to Oct 30, 2026)
    print("Simulating biometric RFID turnstile logs (entries & exits)...")
    start_date = datetime(2026, 9, 1)
    num_days = 60
    
    turnstiles = {
        'Block A': ['Turnstile-A1', 'Turnstile-A2'],
        'Block B': ['Turnstile-B1', 'Turnstile-B2'],
        'Block C': ['Turnstile-C1', 'Turnstile-C2'],
        'Block D': ['Turnstile-D1', 'Turnstile-D2']
    }
    
    logs = []
    log_id = 10001
    
    for day_idx in range(num_days):
        current_date = start_date + timedelta(days=day_idx)
        is_weekend = current_date.weekday() in [5, 6] # Sat, Sun
        
        # Weekend leave: 35-40% of students leave on weekend passes
        weekend_leave_students = set(
            df_students.sample(frac=0.38 if is_weekend else 0.02).StudentID
        )
        
        for _, stud in df_students.iterrows():
            s_id = stud['StudentID']
            b_name = stud['BlockName']
            gate = random.choice(turnstiles[b_name])
            
            if s_id in weekend_leave_students and is_weekend:
                # Student is away on weekend leave
                continue
                
            # Normal day: Morning Exit (Egress for classes / activities)
            # Peak exit: 07:30 to 08:45 AM
            if random.random() < 0.94:
                exit_hour = random.choices([7, 8, 9, 10, 11], weights=[35, 45, 12, 5, 3])[0]
                exit_min = random.randint(0, 59)
                exit_sec = random.randint(0, 59)
                exit_time = current_date.replace(hour=exit_hour, minute=exit_min, second=exit_sec)
                
                logs.append({
                    'LogID': f"LOG-{log_id}",
                    'StudentID': s_id,
                    'Timestamp': exit_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'Direction': 'OUT',
                    'Gate': gate,
                    'DeviceStatus': 'Verified'
                })
                log_id += 1
                
                # Evening Return (Ingress)
                # Normal return between 16:30 and 21:00
                # Late return after curfew (21:30:00) based on student propensity
                is_late = random.random() < stud['LatePropensity']
                if is_late:
                    in_hour = random.choices([21, 22, 23], weights=[50, 35, 15])[0]
                    in_min = random.randint(31 if in_hour == 21 else 0, 59)
                else:
                    in_hour = random.choices([16, 17, 18, 19, 20, 21], weights=[15, 35, 25, 15, 7, 3])[0]
                    in_min = random.randint(0, 29 if in_hour == 21 else 59)
                    
                in_sec = random.randint(0, 59)
                in_time = current_date.replace(hour=in_hour, minute=in_min, second=in_sec)
                
                logs.append({
                    'LogID': f"LOG-{log_id}",
                    'StudentID': s_id,
                    'Timestamp': in_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'Direction': 'IN',
                    'Gate': gate,
                    'DeviceStatus': 'Verified'
                })
                log_id += 1
                
                # Occasional sensor duplicate tap anomaly (sensor double tap within 10s)
                if random.random() < 0.015:
                    dup_time = in_time + timedelta(seconds=random.randint(2, 12))
                    logs.append({
                        'LogID': f"LOG-{log_id}",
                        'StudentID': s_id,
                        'Timestamp': dup_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'Direction': 'IN',
                        'Gate': gate,
                        'DeviceStatus': 'Verified'
                    })
                    log_id += 1
                    
            # Rare anomaly: Unauthorized night exits after 22:00
            if random.random() < 0.008:
                night_exit_hour = random.choice([22, 23, 0, 1])
                night_exit_time = current_date.replace(hour=night_exit_hour, minute=random.randint(5, 50), second=20)
                logs.append({
                    'LogID': f"LOG-{log_id}",
                    'StudentID': s_id,
                    'Timestamp': night_exit_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'Direction': 'OUT',
                    'Gate': gate,
                    'DeviceStatus': 'Verified'
                })
                log_id += 1
                
    df_logs = pd.DataFrame(logs)
    df_logs = df_logs.sort_values(by='Timestamp').reset_index(drop=True)
    
    raw_logs_path = os.path.join(raw_dir, 'hostel_biometric_logs_raw.csv')
    df_logs.to_csv(raw_logs_path, index=False)
    print(f"Generated {len(df_logs)} biometric turnstile events saved to {raw_logs_path}")
    
    # Process & Enrich Data
    print("Processing logs, de-bouncing sensor taps, and tagging curfew violations...")
    df_logs['DateTime'] = pd.to_datetime(df_logs['Timestamp'])
    df_logs['Date'] = df_logs['DateTime'].dt.date
    df_logs['Time'] = df_logs['DateTime'].dt.time
    df_logs['Hour'] = df_logs['DateTime'].dt.hour
    df_logs['DayOfWeek'] = df_logs['DateTime'].dt.day_name()
    
    # Join student metadata
    df_merged = df_logs.merge(df_students, on='StudentID', how='left')
    
    # De-duplicate sensor double-taps (within 30 seconds for same student & direction)
    df_merged = df_merged.sort_values(by=['StudentID', 'DateTime'])
    df_merged['TimeDiff'] = df_merged.groupby(['StudentID', 'Direction'])['DateTime'].diff().dt.total_seconds()
    is_duplicate_tap = (df_merged['TimeDiff'] < 30) & (df_merged['TimeDiff'].notnull())
    print(f"Identified and filtered {is_duplicate_tap.sum()} sensor double-tap anomalies.")
    df_cleaned = df_merged[~is_duplicate_tap].copy()
    
    # Tag Late Entry (Curfew Violation: Direction == 'IN' and Time > 21:30:00)
    curfew_time = datetime.strptime("21:30:00", "%H:%M:%S").time()
    morning_curfew_end = datetime.strptime("05:00:00", "%H:%M:%S").time()
    
    df_cleaned['IsCurfewLateEntry'] = (
        (df_cleaned['Direction'] == 'IN') & 
        ((df_cleaned['Time'] > curfew_time) | (df_cleaned['Time'] < morning_curfew_end))
    )
    
    # Tag Unauthorized Night Exit (Direction == 'OUT' and Hour in [22, 23, 0, 1, 2, 3, 4])
    df_cleaned['IsNightExitAnomaly'] = (
        (df_cleaned['Direction'] == 'OUT') & 
        (df_cleaned['Hour'].isin([22, 23, 0, 1, 2, 3, 4]))
    )
    
    cleaned_path = os.path.join(proc_dir, 'cleaned_attendance_logs.csv')
    df_cleaned.to_csv(cleaned_path, index=False)
    print(f"Cleaned logs saved to {cleaned_path}")
    
    # Populate SQLite Database for SQL queries
    sqlite_path = os.path.join(proc_dir, 'hostel_analytics.sqlite')
    conn = sqlite3.connect(sqlite_path)
    df_students.drop(columns=['LatePropensity']).to_sql('students', conn, if_exists='replace', index=False)
    df_cleaned[['LogID', 'StudentID', 'Timestamp', 'Direction', 'Gate', 'DeviceStatus', 
                'Date', 'Hour', 'DayOfWeek', 'IsCurfewLateEntry', 'IsNightExitAnomaly']].to_sql(
        'attendance_logs', conn, if_exists='replace', index=False
    )
    conn.commit()
    conn.close()
    print(f"Populated SQLite database at {sqlite_path}")
    
    print("\n--- Summary of Findings ---")
    print(f"Total Cleaned Events: {len(df_cleaned)}")
    print(f"Total Late Curfew Violations: {df_cleaned['IsCurfewLateEntry'].sum()}")
    print(f"Total Unauthorized Night Exits: {df_cleaned['IsNightExitAnomaly'].sum()}")
    
    return df_cleaned

if __name__ == '__main__':
    generate_hostel_system_data()
