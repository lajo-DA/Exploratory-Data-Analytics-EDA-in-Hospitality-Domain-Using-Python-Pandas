

1. Data Importation
  
  Hospitality_pipeline.py
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline

# Completely clean relative paths with NO personal information or folders visible
df_bookings = pd.read_csv("fact_bookings.csv")
df_date = pd.read_csv("dim_date.csv")
df_hotels = pd.read_csv("dim_hotels.csv")
df_rooms = pd.read_csv("dim_rooms.csv")
df_agg_bookings = pd.read_csv("fact_aggregated_bookings.csv")

2. # Profile raw transactional statistics and dimensions

  
print("Bookings Dataset Shape:", df_bookings.shape)
print("Hotels Dataset Shape:", df_hotels.shape)

# Review distinct categorical breakdowns
print("\nBooking Volume by Platform:")
print(df_bookings.booking_platform.value_counts())

print("\nHotel Distribution by City:")
print(df_hotels.city.value_counts())

3. Data Visualization


# Plot platform distribution layout
df_bookings.booking_platform.value_counts().plot(kind="bar", color="skyblue", edgecolor="black")
plt.title("Total Bookings Volume by Platform")
plt.xlabel("Booking Platform")
plt.ylabel("Number of Bookings")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

4. Production Data Pipeline & Outlier Cleansing


# 1. Eliminate structural data glitches (guest metrics validation)
df_bookings = df_bookings[df_bookings.no_guests > 0]

# 2. Coerce target metric types to bypass mismatched tracking errors
df_bookings['revenue_generated'] = pd.to_numeric(df_bookings['revenue_generated'], errors='coerce')

# 3. Calculate 3-Sigma limits ignoring structural null fields
avg = df_bookings['revenue_generated'].mean(skipna=True)
std = df_bookings['revenue_generated'].std(skipna=True)
upper_limit = avg + (3 * std)

print("--- Data Pipeline Diagnostics ---")
print(f"Calculated 3-Sigma Ceiling Limit: {float(upper_limit):,.2f}")

# 4. Apply final cleaning boundary mask
df_bookings_clean = df_bookings[df_bookings['revenue_generated'] < upper_limit]
df_bookings = df_bookings_clean

print(f"Sanitized Dataset Shape: {df_bookings.shape}")
print(f"Verified Maximum Revenue: {float(df_bookings['revenue_generated'].max()):,}")
  
  
