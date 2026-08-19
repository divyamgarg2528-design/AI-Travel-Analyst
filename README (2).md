# AI Travel Analyst - Flight Price Exploration

## Project Overview
*(2-3 sentences: what this project does and what problem it solves)*
This project analyzes flight price data to understand which factors drive
ticket prices and to provide actionable insights for travelers.

## Problem Statement
*(What question are you answering? e.g.)*
Flight prices vary widely based on airline, route, number of stops, and
booking timing. This project explores the dataset to identify the biggest
drivers of price and turn them into practical recommendations for travelers.

## Installation Instructions
```bash
git clone <your-repo-url>
cd ai-travel-analyst
pip install -r requirements.txt
python explore_flights.py
```

## Dataset Used
*(Name/link of the dataset, and note that it was the mandatory dataset
provided in the task)*
- Source: [link provided in the task]
- Rows / columns: *(fill in after loading)*

## Methodology
*(Explain your steps in your own words - this matters a lot for grading)*
1. Loaded the raw CSV with pandas.
2. Checked for missing values and duplicates, and cleaned them.
3. Converted text fields (like flight duration, number of stops) into
   numeric fields so they could be analyzed and plotted.
4. Created 5 visualizations to explore relationships between price and
   other variables (airline, stops, route, duration).
5. Computed correlations and summarized key findings.

## Technologies Used
- Python
- pandas
- matplotlib / seaborn

## Results
*(Fill in with your actual findings once you run the script and look at
the charts, e.g.)*
- Flights with more stops tend to cost [more/less], because...
- The most expensive routes are...
- Booking further/closer to the departure date tends to...
- Recommendation for travelers: ...

## Challenges Faced
*(Be honest - e.g. messy duration format, missing values, unfamiliar
column names, etc.)*

## Future Improvements
*(e.g. build a price prediction model - Part 2, add an interactive
dashboard with Streamlit - stretch goal, add more granular route analysis)*

## Screenshots
*(Paste your chart images here once generated, e.g.)*
![Price Distribution](charts/1_price_distribution.png)
