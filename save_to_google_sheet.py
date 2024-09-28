import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Define the scope
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']

creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

print("creds_path: " + str(creds_path))

# Load the credentials from the file
with open(creds_path, 'r') as f:
    creds_json = json.load(f)

creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)

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

# Success message
print("Data successfully saved to Google Sheet!")
