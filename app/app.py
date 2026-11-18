import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

st.set_page_config(
    page_title="Hostel Occupancy & Attendance Portal",
    page_icon="🏢",
    layout="wide"
)

@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'processed', 'cleaned_attendance_logs.csv')
    df = pd.read_csv(data_path)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

st.title("🏢 Hostel Occupancy & Biometric Attendance Analytics Portal")
st.markdown("Developed by **Nithin K S** | *Python • Pandas • SQL • Power BI DAX*")

# Sidebar Filters
st.sidebar.header("🔍 Filter Dashboard")
blocks = ["All Blocks"] + sorted(list(df['BlockName'].unique()))
selected_block = st.sidebar.selectbox("Hostel Block", blocks)

days = ["All Days"] + ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
selected_day = st.sidebar.selectbox("Day of Week", days)

filtered_df = df.copy()
if selected_block != "All Blocks":
    filtered_df = filtered_df[filtered_df['BlockName'] == selected_block]
if selected_day != "All Days":
    filtered_df = filtered_df[filtered_df['DayOfWeek'] == selected_day]

# Top KPI ribbon
c1, c2, c3, c4 = st.columns(4)
total_events = len(filtered_df)
curfew_violations = filtered_df['IsCurfewLateEntry'].sum()
night_exits = filtered_df['IsNightExitAnomaly'].sum()
unique_students = filtered_df['StudentID'].nunique()

c1.metric("Turnstile Events Analyzed", f"{total_events:,}")
c2.metric("Curfew Violations (>9:30 PM)", f"{curfew_violations:,}", delta_color="inverse")
c3.metric("Unauthorized Night Exits", f"{night_exits:,}", delta_color="inverse")
c4.metric("Active Tracked Students", f"{unique_students:,}")

st.divider()

tab1, tab2, tab3 = st.tabs(["🚦 Peak Hours & Traffic Flow", "⚠️ Curfew & Anomaly Surveillance", "👥 Student Offender Directory"])

with tab1:
    st.subheader("Hourly Egress vs Ingress Traffic Flow")
    hourly = filtered_df.groupby(['Hour', 'Direction']).size().unstack(fill_value=0).reset_index()
    fig_hourly = px.bar(
        hourly,
        x='Hour',
        y=['OUT', 'IN'],
        barmode='group',
        labels={'value': 'Turnstile Scans', 'Hour': 'Hour of Day (24-Hour Military Time)'},
        color_discrete_map={'OUT': '#e6550d', 'IN': '#2b83ba'},
        title="Hourly Scan Volume (Peak Morning Egress at 8 AM, Peak Return at 5-6 PM)"
    )
    st.plotly_chart(fig_hourly, use_container_width=True)

with tab2:
    st.subheader("Late Curfew Entries by Hostel Block & Department")
    c_left, c_right = st.columns(2)
    
    with c_left:
        late_by_block = filtered_df[filtered_df['IsCurfewLateEntry'] == True].groupby('BlockName').size().reset_index(name='Violations')
        fig_block = px.pie(late_by_block, names='BlockName', values='Violations', hole=0.4, title="Late Curfew Incidents by Block")
        st.plotly_chart(fig_block, use_container_width=True)
        
    with c_right:
        late_by_day = filtered_df[filtered_df['IsCurfewLateEntry'] == True].groupby('DayOfWeek').size().reset_index(name='Violations')
        fig_day = px.bar(late_by_day, x='DayOfWeek', y='Violations', color='Violations', color_continuous_scale='Reds', title="Late Entries by Day of Week")
        st.plotly_chart(fig_day, use_container_width=True)

with tab3:
    st.subheader("Chronic Curfew Offenders (Repeat Violations > 3)")
    late_df = filtered_df[filtered_df['IsCurfewLateEntry'] == True]
    offender_table = late_df.groupby(['StudentID', 'FullName', 'BlockName', 'RoomNumber', 'Department']).size().reset_index(name='TotalViolations')
    offender_table = offender_table[offender_table['TotalViolations'] >= 3].sort_values(by='TotalViolations', ascending=False)
    
    st.dataframe(offender_table, use_container_width=True, hide_index=True)
