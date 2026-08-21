"""
AI Travel Analyst - Part 1: Exploration
-----------------------------------------
This script:
1. Loads the flight price dataset
2. Cleans and preprocesses it
3. Creates 5+ visualizations
4. Prints out insights about what drives flight prices

HOW TO USE:
1. Download the dataset from the link given in the task PDF and place the
   CSV file in this same folder (rename it to 'flights.csv', or change
   DATA_PATH below).
2. Open the CSV once in Excel/pandas to check the ACTUAL column names -
   datasets like this can vary slightly. Update the COLUMN NAME section
   below if needed.
3. Run: python explore_flights.py
4. Charts will be saved into the 'charts/' folder AND shown on screen.

Make sure you actually read every line here and understand it -
you'll need to explain this in the interview!
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ----------------------------------------------------------------------
# SETUP
# ----------------------------------------------------------------------
DATA_PATH = "flights.csv"          # <-- change if your file has a different name
OUTPUT_DIR = "charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)
sns.set_style("whitegrid")

# ----------------------------------------------------------------------
# STEP 1: LOAD DATA
# ----------------------------------------------------------------------
print("Loading data...")
df = pd.read_csv(DATA_PATH)
print(f"Shape: {df.shape}")
print("\nColumns found in dataset:")
print(df.columns.tolist())
print("\nFirst few rows:")
print(df.head())

# ----------------------------------------------------------------------
# STEP 2: CLEAN / PREPROCESS DATA
# ----------------------------------------------------------------------
# NOTE: Column names below are a common guess (Airline, Source, Destination,
# Duration, Total_Stops, Price, Date_of_Journey). ADJUST these to match
# your actual CSV columns - print(df.columns.tolist()) above will tell you.

print("\nMissing values per column:")
print(df.isnull().sum())

# Drop rows with missing target (price) - can't use rows with no price
if "Price" in df.columns:
    df = df.dropna(subset=["Price"])

# Drop exact duplicate rows
before = len(df)
df = df.drop_duplicates()
print(f"\nDropped {before - len(df)} duplicate rows")

# Example: convert Duration column ("2h 50m") into total minutes, if present
def duration_to_minutes(duration_str):
    """Converts a string like '2h 50m' or '19h' into total minutes."""
    if pd.isna(duration_str):
        return None
    hours, minutes = 0, 0
    parts = str(duration_str).split()
    for p in parts:
        if "h" in p:
            hours = int(p.replace("h", ""))
        elif "m" in p:
            minutes = int(p.replace("m", ""))
    return hours * 60 + minutes

if "Duration" in df.columns:
    df["Duration_Minutes"] = df["Duration"].apply(duration_to_minutes)

# Example: clean Total_Stops into a numeric column, if present
if "Total_Stops" in df.columns:
    stops_map = {
        "non-stop": 0, "1 stop": 1, "2 stops": 2,
        "3 stops": 3, "4 stops": 4
    }
    df["Stops_Num"] = df["Total_Stops"].map(stops_map)
    # Fill anything unmapped with the median
    df["Stops_Num"] = df["Stops_Num"].fillna(df["Stops_Num"].median())

print("\nData cleaned. Final shape:", df.shape)

# ----------------------------------------------------------------------
# STEP 3: VISUALIZATIONS (at least 5 required)
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

print(f"\nCharts saved to '{OUTPUT_DIR}/' folder.")

# ----------------------------------------------------------------------
# STEP 4: PRINT KEY INSIGHTS (fill these in based on YOUR actual results)
# ----------------------------------------------------------------------
print("\n--- INSIGHTS (edit this section after reviewing your charts) ---")
if "Stops_Num" in df.columns:
    corr = df["Stops_Num"].corr(df["Price"])
    print(f"Correlation between number of stops and price: {corr:.2f}")
if "Duration_Minutes" in df.columns:
    corr = df["Duration_Minutes"].corr(df["Price"])
    print(f"Correlation between duration and price: {corr:.2f}")

print("""
TODO for you:
- Look at each chart in the 'charts' folder.
- Write 3-5 sentences per chart about what it shows.
- Note which factors seem to matter most for price (airline? stops? route?).
- Turn these into 'recommendations' for travelers in your README.
""")
