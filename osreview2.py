import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# Set page configuration for a fancy look
st.set_page_config(page_title="SJF Appointment Scheduler", layout="wide")
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://www.med-technews.com/downloads/8696/download/digital%20health.jpg?cb=62a58926fee9a6ec31d2f757983623d4&w=1000&h=');
        background-size: cover;
    }
    </style>
    """, unsafe_allow_html=True)

# Function to implement Shortest Job First (SJF) Scheduling
def sjf_scheduling(jobs, start_time):
    jobs = sorted(jobs, key=lambda x: x['Processing Time'])
    current_time = start_time
    schedule_for_patients = []
    schedule_for_devs = []
    for job in jobs:
        end_time = current_time + timedelta(minutes=job['Processing Time'])
        schedule_for_patients.append({
            'Patient ID': job['Patient ID'],
            'Procedure': job['Procedure'],
            'Start Time': current_time.strftime('%I:%M %p'),
            'End Time': end_time.strftime('%I:%M %p')
        })
        schedule_for_devs.append({
            'Patient ID': job['Patient ID'],
            'Procedure': job['Procedure'],
            'Start Time': current_time,
            'End Time': end_time,
            'Processing Time': job['Processing Time']
        })
        current_time = end_time
    return pd.DataFrame(schedule_for_patients), pd.DataFrame(schedule_for_devs)

# Streamlit App
st.title('Appointment Scheduler Using SJF')

# Display developer information
st.sidebar.markdown("### Project Developers:")
st.sidebar.markdown("1. **Sachin Yadav** - ID: 2341551")
st.sidebar.markdown("2. **Hema C** - ID: 231530")

# Input section for jobs
st.subheader('Enter Job Details:')
num_jobs = st.number_input('Number of Jobs', min_value=1, step=1)

jobs = []
for i in range(num_jobs):
    st.markdown(f"### Job {i+1}")
    default_id = random.randint(1000, 9999)  # Default random patient ID
    patient_id = st.text_input(f'Patient ID for Job {i+1}', value=str(default_id), key=f'patient_id_{i}')
    procedure = st.selectbox(f'Procedure for Job {i+1}', ['MRI', 'CT Scan', 'Blood Test', 'X-Ray', 'Ultrasound'], key=f'procedure_{i}')
    processing_time = st.number_input(f'Processing Time (in minutes) for Job {i+1}', min_value=1, step=1, key=f'processing_time_{i}')
    
    jobs.append({
        'Patient ID': patient_id,
        'Procedure': procedure,
        'Processing Time': processing_time
    })

# Process and show the schedule
if st.button('Generate Schedule'):
    if jobs:
        office_start_time = datetime.today().replace(hour=9, minute=0, second=0, microsecond=0)  # Office starts at 9 AM
        schedule_patients, schedule_devs = sjf_scheduling(jobs, office_start_time)
        st.subheader('Patient Appointment Schedule:')
        st.dataframe(schedule_patients)
        st.subheader('Developer Schedule View:')
        st.dataframe(schedule_devs)
    else:
        st.error("Please enter job details to generate the schedule.")
