import streamlit as st
import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

CSV_FILE = 'blood_pressure_data.csv'

def read_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=['timestamp', 'systolic', 'diastolic', 'weight', 'pulse', 'feeling'])

def append_data(new_data):
    data = read_data()
    data = data.append(new_data, ignore_index=True)
    data.to_csv(CSV_FILE, index=False)

def plot_box(data):
    if not data.empty:
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        data['day'] = data['timestamp'].dt.to_period('D')

        # Restructure the data into long format
        long_data = data.melt(id_vars=['day'], value_vars=['systolic', 'diastolic'], var_name='type', value_name='blood_pressure')

        fig, ax = plt.subplots(figsize=(12, 6))
        ax = sns.boxplot(x='day', y='blood_pressure', hue='type', data=long_data)
        ax.set_title('Blood Pressure Over Time')
        ax.set_xlabel('Day')
        ax.set_ylabel('Blood Pressure')

        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.write("No data to display yet.")
        
def plot_data(data):
    if not data.empty:
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        fig, ax = plt.subplots()
        ax.plot(data['timestamp'], data['systolic'], label='Systolic', marker='o')
        ax.plot(data['timestamp'], data['diastolic'], label='Diastolic', marker='o')
        plt.xlabel('Timestamp')
        plt.ylabel('Blood Pressure')
        plt.title('Blood Pressure Over Time')
        plt.legend()

        # Format x-axis to display days only
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.xticks(rotation=45)

        # Add horizontal threshold lines
        for y in range(100, 141):
            ax.axhline(y, color='gray', linewidth=0.5)

        for y in range(60, 91):
            ax.axhline(y, color='gray', linewidth=0.5)

        st.pyplot(fig)
    else:
        st.write("No data to display yet.")

st.title("Blood Pressure Tracker")

st.sidebar.header("Input Data")
systolic = st.sidebar.number_input("Systolic Pressure", min_value=0, max_value=250, step=1)
diastolic = st.sidebar.number_input("Diastolic Pressure", min_value=0, max_value=150, step=1)
weight = st.sidebar.number_input("Weight (optional)", min_value=0.0, format="%.1f")
pulse = st.sidebar.number_input("Pulse (optional)", min_value=0, max_value=300, step=1)
feeling = st.sidebar.text_input("How do you feel? (optional)")

submit = st.sidebar.button("Submit")

if submit:
    new_data = {'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'systolic': systolic,
                'diastolic': diastolic,
                'weight': weight,
                'pulse': pulse,
                'feeling': feeling}
    append_data(new_data)
    st.sidebar.success("Data submitted successfully!")

data = read_data()
plot_data(data)
plot_box(data)
st.write(data)