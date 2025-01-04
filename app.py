import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load the cleaned data
file_path = r'C:\Users\Lenovo\Downloads\analis new\PRSA_Data_20130301-20170228\cleaned_PRSA_data.csv'
df = pd.read_csv(file_path)

# Convert the year, month, day, and hour columns to a datetime column
df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
df.set_index('datetime', inplace=True)

# Define seasons
def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'

df['season'] = df.index.month.map(get_season)

# Sidebar for navigation
st.sidebar.title("Air Quality Analysis Dashboard")
option = st.sidebar.selectbox("Select Analysis", ["Trend Analysis", "Seasonal Analysis", "Meteorological Analysis"])

# Trend Analysis
if option == "Trend Analysis":
    st.title("Trend of PM2.5 in Various Locations in Beijing (2013-2017)")
    # Resample the data to monthly averages, excluding non-numeric columns
    monthly_avg = df.resample('M').mean(numeric_only=True)
    stations = df['station'].unique()
    
    plt.figure(figsize=(14, 7))
    for station in stations:
        station_data = df[df['station'] == station].resample('M').mean(numeric_only=True)
        plt.plot(station_data.index, station_data['PM2.5'], label=station)
    
    plt.title('Trend of PM2.5 in Various Locations in Beijing (2013-2017)')
    plt.xlabel('Date')
    plt.ylabel('PM2.5')
    plt.legend(title='Station')
    st.pyplot(plt)

# Seasonal Analysis
elif option == "Seasonal Analysis":
    st.title("Seasonal Analysis of PM2.5 in Beijing")
    seasonal_avg = df.groupby('season')['PM2.5'].mean()
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=seasonal_avg.index, y=seasonal_avg.values)
    plt.title('Average PM2.5 by Season in Beijing (2013-2017)')
    plt.xlabel('Season')
    plt.ylabel('Average PM2.5')
    st.pyplot(plt)
    
    summer_pm25 = df[df['season'] == 'Summer']['PM2.5'].dropna()
    winter_pm25 = df[df['season'] == 'Winter']['PM2.5'].dropna()
    t_stat, p_value = stats.ttest_ind(summer_pm25, winter_pm25)
    
    st.write(f"T-statistic: {t_stat}")
    st.write(f"P-value: {p_value}")
    if p_value < 0.05:
        st.write("There is a significant difference in PM2.5 levels between Summer and Winter.")
    else:
        st.write("There is no significant difference in PM2.5 levels between Summer and Winter.")

# Meteorological Analysis
elif option == "Meteorological Analysis":
    st.title("Meteorological Analysis of PM2.5 in Beijing")
    corr_matrix = df[['PM2.5', 'TEMP', 'PRES', 'DEWP', 'WSPM']].corr()
    
    plt.figure(figsize=(10, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation Matrix between PM2.5 and Meteorological Factors')
    st.pyplot(plt)
    
    st.subheader("Scatter Plot of PM2.5 vs Temperature")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='TEMP', y='PM2.5', data=df)
    plt.title('Scatter Plot of PM2.5 vs Temperature')
    plt.xlabel('Temperature (°C)')
    plt.ylabel('PM2.5 (µg/m³)')
    st.pyplot(plt)
    
    st.subheader("Scatter Plot of PM2.5 vs Dew Point")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='DEWP', y='PM2.5', data=df)
    plt.title('Scatter Plot of PM2.5 vs Dew Point')
    plt.xlabel('Dew Point (°C)')
    plt.ylabel('PM2.5 (µg/m³)')
    st.pyplot(plt)
    
    st.subheader("Scatter Plot of PM2.5 vs Wind Speed")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='WSPM', y='PM2.5', data=df)
    plt.title('Scatter Plot of PM2.5 vs Wind Speed')
    plt.xlabel('Wind Speed (m/s)')
    plt.ylabel('PM2.5 (µg/m³)')
    st.pyplot(plt)