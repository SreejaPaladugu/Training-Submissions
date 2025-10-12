#Intermediate 1: Apply Python Data Structures on a real dataset and explain results.
import pandas as pd

# Load a sample COVID-19 dataset from an online source
url = "https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv"
df = pd.read_csv(url)

# Convert DataFrame to list of dictionaries
records = df.to_dict(orient='records')

# Aggregate total confirmed cases per country
country_cases = {}
for record in records:
    country = record['Country']
    cases = record['Confirmed']
    country_cases[country] = country_cases.get(country, 0) + cases

# Sort and get top 5 countries
top_5 = sorted(country_cases.items(), key=lambda x: x[1], reverse=True)[:5]

print("Top 5 countries by confirmed cases:")
for country, total in top_5:
    print(f"{country}: {total}")
