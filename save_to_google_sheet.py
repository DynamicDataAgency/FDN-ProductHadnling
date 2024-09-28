import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe
import os
import json
from dotenv import load_dotenv
from google.oauth2 import service_account

# Load environment variables from .env file
load_dotenv()

# Define the scope for accessing Google Sheets and Google Drive
scopes = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']

# Retrieve the credentials JSON from the environment variable
TYPE = os.getenv("service_account")
PROJECT_ID = os.getenv("project_id")
PRIVATE_KEY_ID = os.getenv("private_key_id")
PRIVATE_KEY = os.getenv("private_key")
CLIENT_EMAIL = os.getenv("client_email")
CLIENT_ID = os.getenv("client_id")
AUTH_URI = os.getenv("auth_uri")
TOKEN_URI = os.getenv("token_uri")
AUTH_PROVIDER_X509_CERT_URL = os.getenv("auth_provider_x509_cert_url")
CLIENT_X509_CERT_URL = os.getenv("client_x509_cert_url")


credentials = service_account.Credentials.from_service_account_info({
        "project_id": os.getenv("project_id"),
        "private_key_id": os.getenv("private_key_id"),
        "private_key": os.getenv("private_key"),
        "client_email": os.getenv("client_email"),
        "client_id": os.getenv("CLIENT_ID"),
        "auth_uri": os.getenv("AUTH_URI"),
        "token_uri": os.getenv("TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
    }, scopes=scopes)

client = gspread.authorize(credentials)

# Load the processed DataFrame
df = pd.read_csv('processed_data.csv')

# Open the Google Sheet (by name or by key)
spreadsheet = client.open("Fanatics_product_import")

# Save the DataFrame to the Google Sheet
worksheet = spreadsheet.get_worksheet(0)
set_with_dataframe(worksheet, df)
print("Data saved to Google Sheet")



