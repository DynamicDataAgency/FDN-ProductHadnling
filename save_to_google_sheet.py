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
PROJECT_ID = os.getenv("PROJECT_ID")
PRIVATE_KEY_ID = os.getenv("private_key_id")
PRIVATE_KEY = os.getenv("private_key")
CLIENT_EMAIL = os.getenv("client_email")
CLIENT_ID = os.getenv("client_id")
AUTH_URI = os.getenv("auth_uri")
TOKEN_URI = os.getenv("token_uri")
AUTH_PROVIDER_X509_CERT_URL = os.getenv("auth_provider_x509_cert_url")
CLIENT_X509_CERT_URL = os.getenv("client_x509_cert_url")

print(TYPE)
print(PROJECT_ID)
print(PRIVATE_KEY_ID)
print(PRIVATE_KEY)
print(CLIENT_EMAIL)
print(CLIENT_ID)
print(AUTH_URI)
print(TOKEN_URI)
print(AUTH_PROVIDER_X509_CERT_URL)
print(CLIENT_X509_CERT_URL)


