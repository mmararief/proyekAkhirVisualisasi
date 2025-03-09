import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
day_df = pd.read_csv("data/day.csv")
hour_df = pd.read_csv("data/hour.csv")

# Dashboard Title
st.title("Bike Sharing Data Analysis")

# Sidebar
st.sidebar.header("Filter Data")
season_filter = st.sidebar.selectbox("Select Season", ["All"] + list(day_df["season"].unique()))

# Filter Data
if season_filter != "All":
    filtered_data = day_df[day_df["season"] == season_filter]
else:
    filtered_data = day_df

# Show Dataset
st.subheader("Dataset Preview")
st.write(filtered_data.head())

# # Visualization 1: Bike Rentals Over Time
# st.subheader("Bike Rentals Over Time")
# plt.figure(figsize=(10, 5))
# sns.lineplot(x=filtered_data["dteday"], y=filtered_data["cnt"], marker="o")
# plt.xticks(rotation=45)
# plt.xlabel("Date")
# plt.ylabel("Total Rentals")
# plt.title("Daily Bike Rentals Trend")
# st.pyplot(plt)

# Visualization 2: Bike Rentals by Weather
st.subheader("Bike Rentals by Weather Condition")
plt.figure(figsize=(8, 5))
sns.boxplot(x=filtered_data["weathersit"], y=filtered_data["cnt"])
plt.xlabel("Weather Condition")
plt.ylabel("Total Rentals")
plt.title("Distribution of Bike Rentals Based on Weather")
st.pyplot(plt)

# Additional Analysis: Rentals by Hour
st.subheader("Bike Rentals by Hour of the Day")
plt.figure(figsize=(10, 5))
sns.lineplot(x=hour_df["hr"], y=hour_df["cnt"], marker="o")
plt.xlabel("Hour of the Day")
plt.ylabel("Total Rentals")
plt.title("Hourly Bike Rental Trend")
st.pyplot(plt)

# Conclusion
st.subheader("Conclusions")
st.write("1. Weather conditions have an impact on the number of rentals.")
st.write("2. Bike rentals peak during specific hours of the day, indicating user preferences.")
