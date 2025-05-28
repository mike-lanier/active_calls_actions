from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import os

csv_path = "data/active_calls.csv"  # your CSV file path inside the repo

# Load and parse webpage data
with urlopen('https://www1.cityoforlando.net/opd/activecalls/activecadpolice.xml') as page:
    bsObj = BeautifulSoup(page, "xml")

# Extract data into DataFrame
data = {
    'incident_id': [call['incident'] for call in bsObj.find_all("CALL")],
    'call_date': [pd.to_datetime(date.get_text()) for date in bsObj.find_all("DATE")],
    'description': [desc.get_text() for desc in bsObj.find_all("DESC")],
    'location': [loc.get_text() for loc in bsObj.find_all("LOCATION")],
    'district': [dist.get_text() for dist in bsObj.find_all("DISTRICT")],
    'department': "OPD"
}

df_new = pd.DataFrame(data)

# Create folder if it doesn't exist
os.makedirs(os.path.dirname(csv_path), exist_ok=True)

if os.path.exists(csv_path):
    df_existing = pd.read_csv(csv_path, parse_dates=['call_date'])
    # Append new rows that are not already in existing CSV (based on incident_id)
    df_combined = pd.concat([df_existing, df_new]).drop_duplicates(subset=['incident_id'])
else:
    df_combined = df_new

df_combined.to_csv(csv_path, index=False)
print(f"Data updated and saved to {csv_path}")