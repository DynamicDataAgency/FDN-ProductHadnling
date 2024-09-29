import os
import json
from dotenv import load_dotenv
from google.oauth2 import service_account
import gspread
from gspread_dataframe import set_with_dataframe
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Define the scope for accessing Google Sheets and Google Drive
scopes = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']

# Retrieve the credentials from environment variables
credentials_dict = {
    "type": os.getenv("TYPE"),
    "project_id": os.getenv("PROJECT_ID"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": os.getenv("PRIVATE_KEY").replace('\\n', '\n'),  # Ensure proper formatting
    "client_email": os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLIENT_ID"),
    "auth_uri": os.getenv("AUTH_URI"),
    "token_uri": os.getenv("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL")
}

# Create credentials object
credentials = service_account.Credentials.from_service_account_info(credentials_dict, scopes=scopes)

# Authorize and create client
client = gspread.authorize(credentials)

try:
    # Open the Google Sheet (by name or by key)
    spreadsheet = client.open("Fanatics_product_import")
    
    # Assuming 'nf' is your DataFrame that you want to save
    # If 'nf' is not defined, you'll need to create or load your DataFrame here
    # For example: nf = pd.DataFrame(...)

    # Save the DataFrame to the Google Sheet
    worksheet = spreadsheet.get_worksheet(0)
    set_with_dataframe(worksheet, nf)
    print("Data saved to Google Sheet successfully")

except Exception as e:
    print(f"An error occurred: {str(e)}")