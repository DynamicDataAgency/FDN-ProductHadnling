import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe
import os

# Define the scope
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']

# Get the Google Application Credentials file path from the environment
creds_path = os.path.expanduser(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

if creds_path is None or not os.path.exists(creds_path):
    raise ValueError(f"GOOGLE_APPLICATION_CREDENTIALS environment variable is not set or the file doesn't exist: {creds_path}")

# Authorize using the credentials file path
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Load the processed DataFrame
df = pd.read_csv('processed_data.csv')

# Open the Google Sheet (by name or by key)
spreadsheet = client.open("Fanatics_product_import")
sheet = spreadsheet.sheet1  

# Clear existing data in the sheet (optional)
sheet.clear()

# Write DataFrame to Google Sheet
set_with_dataframe(sheet, df)
