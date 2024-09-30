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
TYPE = os.getenv("TYPE")
PROJECT_ID = os.getenv("PROJECT_ID")
PRIVATE_KEY_ID = os.getenv("PRIVATE_KEY_ID")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CLIENT_EMAIL = os.getenv("CLIENT_EMAIL")
CLIENT_ID = os.getenv("CLIENT_ID")
AUTH_URI = os.getenv("AUTH_URI")
TOKEN_URI = os.getenv("TOKEN_URI")
AUTH_PROVIDER_X509_CERT_URL = os.getenv("AUTH_PROVIDER_X509_CERT_URL")
CLIENT_X509_CERT_URL = os.getenv("CLIENT_X509_CERT_URL")


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



credentials = service_account.Credentials.from_service_account_info({
        "project_id": os.getenv("PROJECT_ID"),
        "private_key_id": os.getenv("PRIVATE_KEY_ID"),
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDgi/ULG3fwgxbi\npsWUpCwOkEjwAc7aSG4A2eCUTiC8nPEzM628EgjgQXN3Ef9rTqHQ8JNgUTDlzKqo\nnpQ+8JBYeH2s7YVG3IuytakS81vofjAGyTPRk7Cf3ih8TGicjam7kCDdL9FyFPIx\nQpABIKnWbdv4tV/Y/lIrvyCZ9+VH6B0SSK48yIh0nHvyq3EoUQZmbawiWf0m/FPS\n6lrX98xiyMpA9gYQ5eV8JH6iLBQgv8I1tAmheE64B/SufHgTQWAbJO9/uVOxo0Eh\nnfAt602BMyxCAVec1Ctoc6nXJFMwzTef/ppCC8c2jkIXE70zSPYffXtoCiBCfRP5\nZA7sO/jTAgMBAAECggEAGbNLJ6tMLgYC/4wQ/zNPK5eOEZJTZ550oLpPPwo2KwBX\nhwG6N9VkmK5FFfLEZjbIxI5Uf+irDRJA0i3cT9ve2ZFo6PsCjxq9DoZGRLn/4ftX\nad9rg+hAhfu6bIeeTZTVQXd8m3RWp5UIJ2Uz8D0Z00YdsDiqML7jDsjAZX7/Chyr\nGoY9Jo1aHq0VostiyAYPTYMhEMH+/OdeKVD+JysNSwrR7lEKCAPlrKAa58iRVawc\n8MMdhS+WjOit9Zx//X/ZgBvA3eubrwrxkFq8Uxsh5VtBnHk+6waidW5nW8Mlc8o3\nt6JrpPImwKtNbZcfrrBuGWJ+S4FJXshNUMeGb9aZGQKBgQD0QF+AmABEWxi9uDZv\n6SuxQS9UwCPtmvqZk+OorIFEOUApWRaMPMmpgy2xq8oVxyFRO/0z7JqQg1Pnqlyh\nriHzBk862H6SbxKhSCmWnJiAwEcFjvEFHHubf5ONIsiLE4rPfqJmMjjBtnFb9sOS\nNv2BSQtp+8y+OJB4x2L73C7gFQKBgQDrWPJeul5gJw6IwK9Psdur6ltMBcnQGtuR\nvwD6/r9QFd8lWtqVZxr7asqEegkVg+xe23lksiHWwvp2iEoaPjiucH78O4C7gRFE\n65EQKXzy5JT0BwaDkbuWW5ZDvf/vDrKa2cmTnCJ7zANvf4w5qtNUjuQ0pM4yFeFo\nnRsSvj5HRwKBgQCu/nft//khAEtnkdWetGYTZupsRAT5tTGaWrSfIoiywnnPpf5b\nlym8gzl3s+bjV3ntY5dzXi8XHqA8uHgJdmLoZTrapEV60I1+c98oAyXYCOpZdyID\nUXbV379tPOCFlAi9xLLBmXXEg9wP0WopFbDmsdi1pCv6lTgc8G1gmU4USQKBgBy5\nk4OKXcCAo95/Hias/7Hg/dmujy5OSORmGrmH5FPjB4RorWs01W9AXo2C058DphMB\n2LQ4pbavv6A+DEVduM9ZvbYNkS3RmAkAc4k0dyKyUZfjT6E5ZVr5vMJx604DTjtm\nP5s7oF3ZzcWLHNNhDUAx3JqsTtqAHy4EluxXugQ7AoGAUQe4xZjlRcsWLCgAc1UP\nfc8YsE0ctVpsYPb9c/Yzh7uVnrCHQ1QVD4aSf6TjGtRMnVgQXlR40y4S7Tg727x9\nlv+jYmK7RLKvWxgi5AIWQnz8QqWso/XsmFCmG+2XvLJ/jW+Vfcu27D0ROlQb4RKI\nV6YQkl6+DGwtHVECtRA68Bo=\n-----END PRIVATE KEY-----\n",
        "client_email": os.getenv("CLIENT_EMAIL"),
        "client_id": os.getenv("CLIENT_ID"),
        "auth_uri": os.getenv("AUTH_URI"),
        "token_uri": os.getenv("TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
    }, scopes=scopes)



creds = ServiceAccountCredentials.from_json_keyfile_name("crds.json") 

client = gspread.authorize(creds)

# Open the Google Sheet (by name or by key)
spreadsheet = client.open("Fanatics_product_import")	

# create same dataframe
data = {'name': ['Tom', 'Nick', 'John', 'Alice'], 'Age': [20, 21, 19, 18]}

# Save the DataFrame to the Google Sheet
worksheet = spreadsheet.get_worksheet(0)

set_with_dataframe(worksheet, data)

print("Data saved to Google Sheet")

