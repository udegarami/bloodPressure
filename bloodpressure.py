import streamlit as st
import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt

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

def plot_data(data):
    if not data.empty:
        fig, ax = plt.subplots()
        ax.plot(data['timestamp'], data['systolic'], label='Systolic', marker='o')
        ax.plot(data['timestamp'], data['diastolic'], label='Diastolic', marker='o')
        plt.xlabel('Timestamp')
        plt.ylabel('Blood Pressure')
        plt.title('Blood Pressure Over Time')
        plt.legend()
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
st.write(data)