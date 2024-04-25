import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob

# Load data
@st.cache_data
def load_data(path):
    file_list = glob.glob(path)

    # Initialize an empty list to hold the dataframes
    df_list = []

    # Loop over the list of files and read each one into a dataframe
    for file in file_list:
        df = pd.read_csv(file)
        df_list.append(df)

    # Concatenate all the dataframes in the list into a single dataframe
    data = pd.concat(df_list, ignore_index=True)
    return data

data = load_data('../data/*.csv')

# Sidebar
# Convert 'Timestamp' column to datetime type
from datetime import datetime

# Convert 'Timestamp' column to datetime type
data['Timestamp'] = pd.to_datetime(data['Timestamp'])

# Set default value to the minimum and maximum timestamp in your data
start_date = st.sidebar.date_input('Start Date', value=data['Timestamp'].min().date(), min_value=data['Timestamp'].min().date(), max_value=data['Timestamp'].max().date())
end_date = st.sidebar.date_input('End Date', value=data['Timestamp'].max().date(), min_value=start_date, max_value=data['Timestamp'].max().date())

# Convert date to datetime
start_date = pd.Timestamp(datetime.combine(start_date, datetime.min.time()))
end_date = pd.Timestamp(datetime.combine(end_date, datetime.max.time()))

st.sidebar.title('Filters')
# Filter data
filtered_data = data[(data['Timestamp'] >= start_date) & (data['Timestamp'] <= end_date)]
# Display data
st.title('Solar Radiation Measurement Data Dashboard')

st.header('Overview')
st.write('Total Observations:', len(filtered_data))
st.write('Average Global Horizontal Irradiance (GHI):', filtered_data['GHI'].mean(), 'W/m²')

# Line chart for GHI over time
st.header('Global Horizontal Irradiance (GHI) over Time')
plt.figure(figsize=(10, 6))
plt.plot(filtered_data['Timestamp'], filtered_data['GHI'])
plt.xlabel('Timestamp')
plt.ylabel('GHI (W/m²)')
plt.title('GHI over Time')
st.pyplot(plt)

# Scatter plot for DNI vs DHI
st.header('Direct Normal Irradiance (DNI) vs Diffuse Horizontal Irradiance (DHI)')
plt.figure(figsize=(8, 6))
plt.scatter(filtered_data['DNI'], filtered_data['DHI'])
plt.xlabel('DNI (W/m²)')
plt.ylabel('DHI (W/m²)')
plt.title('DNI vs DHI')
st.pyplot(plt)

# Bar chart for cleaning events
st.header('Cleaning Events')
cleaning_counts = filtered_data['Cleaning'].value_counts()
st.bar_chart(cleaning_counts)

# Additional insights
st.header('Additional Insights')

# Add more insights, visualizations, and analysis as needed

# Raw data

st.header('Raw Data')
half_length = len(filtered_data) // 2  # Compute the halfway point
st.write(filtered_data.head(half_length))  # Display only the first half of the data
