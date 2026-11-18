import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def create_visualizations():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'processed', 'cleaned_attendance_logs.csv')
    viz_dir = os.path.join(base_dir, 'visualizations')
    os.makedirs(viz_dir, exist_ok=True)
    
    print("Loading cleaned hostel logs for visualization...")
    df = pd.read_csv(data_path)
    
    sns.set_theme(style="whitegrid")
    
    # 1. Peak Hours Ingress vs Egress Distribution
    plt.figure(figsize=(11, 5))
    hourly_traffic = df.groupby(['Hour', 'Direction']).size().unstack(fill_value=0)
    hourly_traffic = hourly_traffic.reindex(range(24), fill_value=0)
    
    x = np.arange(24)
    width = 0.40
    
    out_vals = hourly_traffic['OUT'].values if 'OUT' in hourly_traffic else np.zeros(24)
    in_vals = hourly_traffic['IN'].values if 'IN' in hourly_traffic else np.zeros(24)
    
    plt.bar(x - width/2, out_vals, width=width, label='Egress (Exits)', color='#e6550d', alpha=0.9)
    plt.bar(x + width/2, in_vals, width=width, label='Ingress (Entries)', color='#2b83ba', alpha=0.9)
    
    # Annotate morning and evening peaks
    plt.annotate('Morning Class Peak\n(7:30 - 8:45 AM)', xy=(8, hourly_traffic.loc[8, 'OUT']), 
                 xytext=(9.5, hourly_traffic.loc[8, 'OUT'] - 300),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=7),
                 fontweight='bold', fontsize=9)
                 
    plt.annotate('Evening Return Peak\n(5:00 - 6:30 PM)', xy=(17, hourly_traffic.loc[17, 'IN']), 
                 xytext=(13.5, hourly_traffic.loc[17, 'IN'] + 200),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=7),
                 fontweight='bold', fontsize=9)
                 
    plt.axvline(21.5, color='red', linestyle='--', linewidth=1.5, label='Curfew Deadline (9:30 PM)')
    
    plt.title('Hourly Hostel Turnstile Traffic: Identifying Gate Congestion & Peak Hours', fontsize=13, fontweight='bold', pad=15)
    plt.xlabel('Hour of Day (24-Hour Military Time)', fontweight='bold')
    plt.ylabel('Turnstile Scans Volume', fontweight='bold')
    plt.xticks(x)
    plt.legend(frameon=True, loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, 'hourly_traffic_distribution.png'), dpi=300)
    plt.close()
    
    # 2. Curfew Late Entry Violations by Block
    plt.figure(figsize=(9, 5))
    late_entries = df[df['IsCurfewLateEntry'] == True]
    block_late = late_entries.groupby(['BlockName', 'Gender']).size().reset_index(name='Violations')
    
    colors = ['#1f77b4', '#1f77b4', '#e377c2', '#e377c2']
    bars = plt.bar(block_late['BlockName'], block_late['Violations'], color=colors, width=0.55)
    plt.title('Curfew Late-Entry Violations (>9:30 PM) by Hostel Block', fontsize=13, fontweight='bold', pad=15)
    plt.xlabel('Hostel Block', fontweight='bold')
    plt.ylabel('Total Late Entry Incidents', fontweight='bold')
    
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 5, f"{int(yval)}", ha='center', va='bottom', fontweight='bold')
        
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, 'late_entry_trends_by_block.png'), dpi=300)
    plt.close()
    
    # 3. Daily Attendance Rate Trend across 60 Days
    plt.figure(figsize=(12, 5))
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Daily in-hostel attendance count: students who registered at least one IN or were present
    daily_present = df[df['Direction'] == 'IN'].groupby('Date')['StudentID'].nunique()
    total_students = 450
    daily_att_rate = (daily_present / total_students) * 100
    
    plt.plot(daily_att_rate.index, daily_att_rate.values, color='#2ca02c', linewidth=2, marker='o', markersize=3, label='Daily Attendance %')
    plt.axhline(daily_att_rate.mean(), color='navy', linestyle='--', linewidth=1.5, label=f'Average Rate ({daily_att_rate.mean():.1f}%)')
    
    # Highlight weekend dips
    plt.title('60-Day Hostel Daily Attendance Rate Trend (Weekday vs Weekend Outings)', fontsize=13, fontweight='bold', pad=15)
    plt.xlabel('Date (Sept - Oct 2026)', fontweight='bold')
    plt.ylabel('Attendance / Occupancy Rate (%)', fontweight='bold')
    plt.ylim(40, 105)
    plt.legend(loc='lower left', frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, 'daily_attendance_rate_trend.png'), dpi=300)
    plt.close()
    
    # 4. Turnstile Traffic Heatmap (Day of Week vs Hour)
    plt.figure(figsize=(11, 6))
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap_data = df.pivot_table(index='DayOfWeek', columns='Hour', values='LogID', aggfunc='count').reindex(days_order).fillna(0)
    
    sns.heatmap(heatmap_data, cmap='YlOrRd', annot=False, cbar_kws={'label': 'Hourly Event Volume'})
    plt.title('Unusual Movement & Traffic Heatmap: Day of Week vs. Hour of Day', fontsize=13, fontweight='bold', pad=15)
    plt.xlabel('Hour of Day', fontweight='bold')
    plt.ylabel('Day of Week', fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, 'unusual_movement_heatmap.png'), dpi=300)
    plt.close()
    
    print(f"All visualizations saved to {viz_dir} successfully!")

if __name__ == '__main__':
    create_visualizations()
