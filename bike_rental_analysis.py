import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px

# Import CSV with renamed columns
df = pd.read_csv("bike_data.csv")

# Clean up some columns
# Convert date to datetime
df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")

# Create a datetime column combining date and hour
df["datetime"] = df["date"] + pd.to_timedelta(df["hour"], unit="h")

# Set the option to allow no silent downcasting
pd.set_option('future.no_silent_downcasting', True)

# Map 'is_holiday' values to boolean
df["is_holiday"] = df["is_holiday"].replace({"No Holiday": False, "Holiday": True}).astype(bool)

# Map 'is_functioning' values to boolean
df["is_functioning"] = df["is_functioning"].replace({"No": False, "Yes": True}).astype(bool)

# Only keep observations where the system is functioning
df = df.query("is_functioning")

# Create a line plot of rented bikes over time
px.line(df, x="datetime", y="n_rented_bikes")

# Calculate the total number of rented bikes per day
by_day = df.groupby("date", as_index=False).agg({"n_rented_bikes": "sum"})

# Create a line plot showing total number of bikes per day over time
px.line(by_day, x="date", y="n_rented_bikes")

# Group by season and date, then calculate total rented bikes per day
by_day_season = df.groupby(["date", "season"], as_index=False).agg({"n_rented_bikes": "sum"})

# Create a line plot showing the total number of bikes per day by season
px.line(by_day_season, x="date", y="n_rented_bikes", color="season")

# Query df to only keep observations at noon
noon_rides = df.query("hour == 12")

# Create a scatter plot showing temperature against number of rented bikes with a trendline
px.scatter(noon_rides, x='temperature_celsius', y='n_rented_bikes', trendline="lowess")

# Calculate the average number of rented bikes per hour
time_of_day = df.groupby("hour", as_index=False).agg({"n_rented_bikes": "mean"})

# Create a bar chart showing the usage pattern
px.bar(time_of_day, x="hour", y="n_rented_bikes")

# Group by hour and season, then calculate the average number of rented bikes
time_of_day_season = df.groupby(["hour", "season"], as_index=False).agg({"n_rented_bikes": "mean"})

# Create a bar chart showing the usage pattern per season
px.bar(time_of_day_season, x="hour", y="n_rented_bikes", color="season", facet_col="season")

# Define New Year's dates
new_years_start = datetime(2017, 12, 31, 12)
new_years_end = datetime(2018, 1, 1, 12)
new_year = df.query("@new_years_start <= datetime <= @new_years_end")

# Show usage pattern for New Year's data
px.bar(new_year, x='datetime', y='n_rented_bikes')
