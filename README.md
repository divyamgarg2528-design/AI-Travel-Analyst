# AI Travel Analyst - Flight Price Exploration

## Project Overview
This project analyzes flight price data to understand which factors drive
ticket prices and to provide actionable insights for travelers.

## Problem Statement
Flight prices vary widely based on airline, route, number of stops, and
booking timing. This project explores the dataset to identify the biggest
drivers of price and turn them into practical recommendations for travelers.

## Installation Instructions
```bash
git clone https://github.com/divyamgarg2528-design/AI-Travel-Analyst.git
cd ai-travel-analyst
pip install -r requirements.txt
python explore_flights.py
```

## Dataset Used
- Source: https://drive.google.com/file/d/1tNUDxjXHzbRXe8CQdIoyJWh8OweGW0rR/view?usp=sharing
- Rows / columns: 93,083 rows x 20 columns, including Flight_ID, Airline,
  Source, Destination, Departure_Date, Duration, Total_Stops, Distance_km,
  Travel_Class, Days_Before_Departure, Season, Weekday, Aircraft_Type,
  Booking_Channel, Passenger_Count, Price.

## Methodology
1. Loaded the raw Excel file with pandas.
2. Checked for missing values and duplicates, and cleaned them (dropped
   1,864 duplicate rows).
3. Cleaned the `Price` column, which was stored as text (e.g. `"Rs.
   151,632.89"`), stripping the currency prefix and commas and converting
   it to a numeric value.
4. Normalized `Airline` names (stripped whitespace, standardized casing)
   so entries like `"Qatar Airways"`, `"QATAR AIRWAYS"`, and
   `"qatar airways"` are treated as the same airline instead of three.
5. Converted `Duration` (e.g. `"2h 50 min"`) into total minutes using a
   regex-based parser, and mapped `Total_Stops` into a numeric column.
6. Created 7 visualizations to explore relationships between price and
   other variables (airline, stops, route, duration, travel class,
   booking lead time).
7. Computed summary statistics and correlations, and saved the key
   numbers to `charts/summary.txt` for easy reference.

## Technologies Used
- Python
- pandas
- matplotlib / seaborn
- openpyxl (for reading the Excel dataset)

## Results
- **Airline / route type is the biggest price driver.** Airlines split
  into two clear groups: budget/domestic carriers (IndiGo, SpiceJet,
  AirAsia, GoFirst, Air India) cluster near the bottom on price, while
  premium/international carriers (Singapore Airlines, Qatar Airways,
  Emirates, British Airways, Lufthansa) range from near-0 up to
  ₹1,000,000+.
- **Number of stops barely affects price** (correlation ≈ 0.06) — contrary
  to the common assumption that non-stop flights cost more.
- **Duration correlates fairly strongly with price** (≈ 0.67), but this
  is mostly a side effect of route type: budget/domestic flights show
  price rising steadily with duration, while premium/international
  flights form a separate cluster that's expensive regardless of length.
- **Most expensive routes are long-haul international ones** (e.g.
  JFK↔India, London↔India, Doha↔London, Sydney routes), consistent with
  the airline-tier finding above.
- **Recommendation for travelers:** airline/route tier matters far more
  than number of stops when trying to save money — comparing budget vs.
  premium carriers on the same route is likely to save more than
  avoiding a layover.
- **Travel class:**First and Business have similar median prices (~₹150–180k) and are clearly higher than Premium Economy and Economy. Economy has the lowest   median (~₹40k). But there's heavy overlap — every class has outliers stretching up toward ₹1,000,000, so travel class shifts the typical price but doesn't cleanly separate it.
- **Booking lead time:**No real trend. There's a dense, flat band of budget-priced flights (under ~₹200k) spread evenly across the entire 0–180 day range — booking early or late doesn't move that price band at all. There's also a scattered cluster of expensive flights (₹300k+) that's noticeably denser in the 0–50 day range and thins out further out — so premium/international bookings appear more concentrated closer to departure, but this isn't a "book early to save money" pattern; if anything it's closer to the opposite.

## Challenges Faced
- The `Price` column was stored as text with a currency prefix and
  thousands separators (`"Rs. 151,632.89"`), which needed cleaning before
  any numeric analysis or plotting could work.
- The `Duration` column had inconsistent formatting (`"2h 50 min"` vs.
  `"2h50m"`), which required a regex-based parser instead of simple
  string splitting.
- The dataset file was actually an Excel spreadsheet despite an initial
  `.csv` extension, requiring `pd.read_excel` (and `openpyxl`) instead of
  `pd.read_csv`.
- Some airline names appeared multiple times with different capitalization
  (e.g. `"Qatar Airways"`, `"QATAR AIRWAYS"`, `"qatar airways"`), which
  would have been treated as separate airlines. Fixed by normalizing
  whitespace and casing right after loading the data.

## Future Improvements
- Build a price prediction model (Part 2).
- Add an interactive dashboard with Streamlit (stretch goal).
- Add more granular route analysis (e.g. by season or booking channel).

## Screenshots
![Price Distribution](charts/1_price_distribution.png)
![Price by Airline](charts/2_price_by_airline.png)
![Price vs Stops](charts/3_price_vs_stops.png)
![Price by Route](charts/4_price_by_route.png)
![Duration vs Price](charts/5_duration_vs_price.png)
![Price by Travel Class](charts/6_price_by_travel_class.png)
![Days Before Departure vs Price](charts/7_price_vs_days_before_departure.png)
