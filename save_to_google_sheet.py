import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define the scope for accessing Google Sheets and Google Drive
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']

# Retrieve the credentials JSON from the environment variable
creds_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Parse the JSON string into a Python dictionary
creds_dict = json.loads(creds_json)

# Authorize with the credentials
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Load the processed DataFrame
df = pd.read_csv('processed_data.csv')

# Open the Google Sheet (by name or by key)
spreadsheet = client.open("Fanatics_product_import")
