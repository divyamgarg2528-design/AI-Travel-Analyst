"""
AI Travel Analyst - Part 1: Exploration
-----------------------------------------
This script:
1. Loads the flight price dataset
2. Cleans and preprocesses it
3. Creates 5+ visualizations
4. Prints out insights about what drives flight prices

HOW TO USE:
1. Place your dataset file in this same folder, named 'flights.xlsx'
   (or change DATA_PATH below to match your file name/format).
2. Run: python explore_flights.py
3. Charts will be saved into the 'charts/' folder.

Make sure you actually read every line here and understand it -
you'll need to explain this in the interview!
"""

from __future__ import annotations

import re
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ----------------------------------------------------------------------
# SETUP
# ----------------------------------------------------------------------
DATA_PATH = "flights.xlsx"         # <-- the dataset is an Excel file
OUTPUT_DIR = "charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)
sns.set_style("whitegrid")

# ----------------------------------------------------------------------
# STEP 1: LOAD DATA
# ----------------------------------------------------------------------
print("Loading data...")
try:
    df = pd.read_excel(DATA_PATH)  # read_excel, not read_csv, since it's .xlsx
except FileNotFoundError:
    sys.exit(
        f"ERROR: Could not find '{DATA_PATH}'.\n"
        f"Make sure the dataset file is in this same folder and named "
        f"exactly '{DATA_PATH}' (or update DATA_PATH at the top of this "
        f"script to match your file's name)."
    )
print(f"Shape: {df.shape}")
print("\nColumns found in dataset:")
print(df.columns.tolist())
print("\nFirst few rows:")
print(df.head())

# ----------------------------------------------------------------------
# STEP 2: CLEAN / PREPROCESS DATA
# ----------------------------------------------------------------------
print("\nMissing values per column:")
print(df.isnull().sum())

# Clean Price column: it's stored as text like "Rs. 151,632.89" -
# strip the currency prefix and thousands-separator commas, then convert
# to an actual number so we can plot/analyze it.
# NOTE: checking "not already numeric" (rather than dtype == object) so
# this also works on newer pandas versions that may load text columns
# as a dedicated "string" dtype instead of plain "object".
if "Price" in df.columns and not pd.api.types.is_numeric_dtype(df["Price"]):
    df["Price"] = (
        df["Price"]
        .astype(str)
        .str.replace("Rs.", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

# Drop rows with missing target (price) - can't use rows with no price
if "Price" in df.columns:
    df = df.dropna(subset=["Price"])

# Normalize Airline casing: the raw data has the same airline written as
# "Qatar Airways", "QATAR AIRWAYS", and "qatar airways" - these all mean
# the same airline but pandas treats them as separate groups. Stripping
# whitespace and title-casing merges them into one consistent category.
if "Airline" in df.columns:
    df["Airline"] = df["Airline"].astype(str).str.strip().str.title()

# Drop exact duplicate rows
before = len(df)
df = df.drop_duplicates()
print(f"\nDropped {before - len(df)} duplicate rows")

# Convert Duration column ("2h 50m", "2h 50 min", "19h", etc.)
# into total minutes, if present. Uses regex so it's tolerant of spacing
# and whether it says "m" or "min".
def duration_to_minutes(duration_str: str | float | None) -> int | None:
    """Converts a duration string into total minutes, handling formats
    like '2h 50m', '2h 50 min', '19h', '45m', etc."""
    if pd.isna(duration_str):
        return None
    s = str(duration_str)
    hours_match = re.search(r"(\d+)\s*h", s)
    minutes_match = re.search(r"(\d+)\s*m", s)  # matches "m" or "min"
    hours = int(hours_match.group(1)) if hours_match else 0
    minutes = int(minutes_match.group(1)) if minutes_match else 0
    if hours == 0 and minutes == 0:
        return None  # couldn't parse anything usable
    return hours * 60 + minutes

if "Duration" in df.columns:
    df["Duration_Minutes"] = df["Duration"].apply(duration_to_minutes)

# Clean Total_Stops into a numeric column, if present
if "Total_Stops" in df.columns:
    stops_map = {
        "non-stop": 0, "1 stop": 1, "2 stops": 2,
        "3 stops": 3, "4 stops": 4
    }
    df["Stops_Num"] = df["Total_Stops"].map(stops_map)
    # Fill anything unmapped with the median
    df["Stops_Num"] = df["Stops_Num"].fillna(df["Stops_Num"].median())

# Clean Days_Before_Departure: it's stored as text like "11 days" -
# extract just the leading number and convert it to a numeric value.
if "Days_Before_Departure" in df.columns and not pd.api.types.is_numeric_dtype(
    df["Days_Before_Departure"]
):
    df["Days_Before_Departure"] = (
        df["Days_Before_Departure"]
        .astype(str)
        .str.extract(r"(\d+)")[0]
    )
    df["Days_Before_Departure"] = pd.to_numeric(
        df["Days_Before_Departure"], errors="coerce"
    )

print("\nData cleaned. Final shape:", df.shape)

# ----------------------------------------------------------------------
# STEP 3: SUMMARY STATISTICS
# ----------------------------------------------------------------------
print("\n--- Price summary statistics ---")
print(df["Price"].describe())

if "Airline" in df.columns:
    print("\n--- Median price by airline (highest to lowest) ---")
    print(df.groupby("Airline")["Price"].median().sort_values(ascending=False))

if "Travel_Class" in df.columns:
    print("\n--- Median price by travel class ---")
    print(df.groupby("Travel_Class")["Price"].median().sort_values(ascending=False))

if "Season" in df.columns:
    print("\n--- Flight count by season ---")
    print(df["Season"].value_counts())

# ----------------------------------------------------------------------
# STEP 4: VISUALIZATIONS (at least 5 required)
# ----------------------------------------------------------------------

# 1. Price distribution
plt.figure(figsize=(8, 5))
sns.histplot(df["Price"], bins=40, kde=True)
plt.title("Distribution of Flight Prices")
plt.xlabel("Price")
plt.savefig(f"{OUTPUT_DIR}/1_price_distribution.png")
plt.close()

# 2. Price by airline
if "Airline" in df.columns:
    plt.figure(figsize=(10, 6))
    order = df.groupby("Airline")["Price"].median().sort_values(ascending=False).index
    sns.boxplot(data=df, x="Price", y="Airline", order=order)
    plt.title("Price Distribution by Airline")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/2_price_by_airline.png")
    plt.close()

# 3. Price vs number of stops
if "Stops_Num" in df.columns:
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df, x="Stops_Num", y="Price")
    plt.title("Price vs Number of Stops")
    plt.xlabel("Number of Stops")
    plt.savefig(f"{OUTPUT_DIR}/3_price_vs_stops.png")
    plt.close()

# 4. Price by route (Source -> Destination)
if "Source" in df.columns and "Destination" in df.columns:
    plt.figure(figsize=(10, 6))
    route_price = (
        df.groupby(["Source", "Destination"])["Price"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )
    route_price.plot(kind="barh")
    plt.title("Top 10 Most Expensive Routes (Average Price)")
    plt.xlabel("Average Price")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/4_price_by_route.png")
    plt.close()

# 5. Duration vs Price
if "Duration_Minutes" in df.columns:
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x="Duration_Minutes", y="Price", alpha=0.4)
    plt.title("Flight Duration vs Price")
    plt.xlabel("Duration (minutes)")
    plt.savefig(f"{OUTPUT_DIR}/5_duration_vs_price.png")
    plt.close()

# 6. Price by travel class
if "Travel_Class" in df.columns:
    plt.figure(figsize=(8, 5))
    order = df.groupby("Travel_Class")["Price"].median().sort_values(ascending=False).index
    sns.boxplot(data=df, x="Travel_Class", y="Price", order=order)
    plt.title("Price Distribution by Travel Class")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/6_price_by_travel_class.png")
    plt.close()

# 7. Price vs days before departure (does booking early save money?)
if "Days_Before_Departure" in df.columns:
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x="Days_Before_Departure", y="Price", alpha=0.4)
    plt.title("Days Before Departure vs Price")
    plt.xlabel("Days Before Departure (booking lead time)")
    plt.savefig(f"{OUTPUT_DIR}/7_price_vs_days_before_departure.png")
    plt.close()

print(f"\nCharts saved to '{OUTPUT_DIR}/' folder.")

# ----------------------------------------------------------------------
# STEP 5: PRINT KEY INSIGHTS (fill these in based on YOUR actual results)
# ----------------------------------------------------------------------
print("\n--- INSIGHTS (edit this section after reviewing your charts) ---")

# Columns to correlate against Price - add more here if you engineer
# other numeric features later.
CORR_COLUMNS = ["Stops_Num", "Duration_Minutes", "Days_Before_Departure"]

summary_lines = [
    "AI Travel Analyst - Summary of Findings",
    "=" * 40,
    f"Final cleaned shape: {df.shape[0]} rows x {df.shape[1]} columns",
    "",
    "Correlations with Price:",
]

for col in CORR_COLUMNS:
    if col in df.columns:
        corr = df[col].corr(df["Price"])
        line = f"  {col} vs Price: {corr:.2f}"
        print(f"Correlation between {col} and price: {corr:.2f}")
        summary_lines.append(line)


summary_path = os.path.join(OUTPUT_DIR, "summary.txt")
with open(summary_path, "w", encoding="utf-8") as f:
    f.write("\n".join(summary_lines) + "\n")
print(f"\nSummary saved to '{summary_path}'.")


