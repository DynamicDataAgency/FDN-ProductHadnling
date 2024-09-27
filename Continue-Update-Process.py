#!/usr/bin/env python
# coding: utf-8

# ### Query FTP

# ##### jupyter nbconvert --to script Continue-Update-Process.ipynb

# In[2]:


import ftplib
import os
import time

# FTP server details
ftp_server = "products.impact.com"
ftp_user = "ps-ftp_5567077"
ftp_password = "6r%]mobnH6"
ftp_directory = "/Fanatics-(Global)/"
file_to_download = "Fanatics-Product-Catalog_IR.txt.gz"  # Specify the file to download

# Local directory to save the file
local_directory = "data-update-process"
os.makedirs(local_directory, exist_ok=True)  # Create the directory if it doesn't exist

max_retries = 3
retry_delay = 5  # Delay in seconds between retries

def download_file():
    """Attempt to connect to FTP and download the specified file."""
    try:
        # Connect to the FTP server
        ftp = ftplib.FTP(ftp_server)
        ftp.set_debuglevel(2)  # Enable FTP command logging
        ftp.set_pasv(True)  # Enable passive mode

        ftp.login(user=ftp_user, passwd=ftp_password)
        ftp.cwd(ftp_directory)

        # List files in the directory
        files = ftp.nlst()
        print("Files in the directory:")
        for file in files:
            print(file)

        # Download only the specified file
        if file_to_download in files:
            local_filename = os.path.join(local_directory, file_to_download)  # Save in the folder
            with open(local_filename, 'wb') as local_file:
                ftp.retrbinary('RETR ' + file_to_download, local_file.write)
                print(f"Downloaded {file_to_download} to {local_directory}")
        else:
            print(f"{file_to_download} not found in the directory.")
        
        ftp.quit()  # Ensure connection is closed

    except ftplib.all_errors as e:
        print(f"FTP error: {e}")
        raise  # Raise the error to be handled by the retry mechanism


# Retry mechanism
for attempt in range(max_retries):
    try:
        download_file()  # Call the function to perform the FTP download
        break  # If the download succeeds, exit the retry loop
    except (ftplib.error_temp, ConnectionResetError) as e:
        print(f"Temporary error occurred: {e}. Retrying ({attempt + 1}/{max_retries})...")
        if attempt == max_retries - 1:
            print("Max retries reached. Exiting.")
            raise e  # Re-raise the exception if all retries fail
        time.sleep(retry_delay)  # Wait before retrying


# ### Decompress downloaded file

# In[3]:


import gzip
import shutil
import os

# Directory containing the downloaded .txt.gz files
directory = os.path.join(os.getcwd(), "data-update-process")  # Path to the downloaded files

# Decompress each .txt.gz file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.txt.gz'):
        local_gz_filename = os.path.join(directory, filename)
        local_txt_filename = os.path.join(directory, filename[:-3])  # Remove the .gz extension

        # Decompress the .txt.gz file to .txt
        with gzip.open(local_gz_filename, 'rb') as f_in:
            with open(local_txt_filename, 'wb') as f_out: 
                shutil.copyfileobj(f_in, f_out)
                print(f"Decompressed {local_gz_filename} to {local_txt_filename}")


# ### Convert to a Pandas DataFrame

# In[57]:


import pandas as pd


# Get the current working directory
directory = os.path.join(os.getcwd(), "data-update-process")

# Path to the decompressed .txt file
local_txt_filename = os.path.join(directory, "Fanatics-Product-Catalog_IR.txt")

# Load the decompressed .txt file into a Pandas DataFrame
if os.path.exists(local_txt_filename):
    # Assuming the file is tab-delimited, adjust the delimiter if necessary
    df = pd.read_csv(local_txt_filename, delimiter='\t', low_memory=False)
    print(df.head())  # Display the first 5 rows
else:
    print(f"{local_txt_filename} does not exist.")


# ### Filter needed products

# In[58]:


df= df[df["Category"] == "NFL"]
df=df.head(2000)


# In[59]:


df.shape


# ### Transformations to fit Shopify product import

# In[60]:


# Count the occurrences of each value in the 'Text3' column of the 'nf' dataframe
# text3_counts = nf['Text3'].value_counts()

# Print the top 60 values
#  print(text3_counts.head(60))

nf = df.loc[:, ['Unique Merchant SKU', 'Product Name', 'Product URL', 'Image URL', 'Current Price', 'Original Price', 'Product Description', 'Gender', 'Text1', 'Text2', 'Text3','Size']]

rename_dict = {
    'Unique Merchant SKU': 'ID',
    'Product Name': 'Title',
    'Product URL': 'Metafield: custom.product_url [url]',
    'Image URL': 'Image Src',
    'Current Price': 'Variant Price',
    'Original Price': 'Variant Compare At Price',
    'Product Description': 'Body HTML',
    'Gender': 'Metafield: custom.product_gender [single_line_text_field]',
    'Text1': 'Metafield: custom.text1 [single_line_text_field]',
    'Text2': 'Metafield: custom.text2 [single_line_text_field]',
    'Text3': 'Tags',
    'Size': 'Metafield: custom.sizes [single_line_text_field]'
}

nf = nf.rename(columns=rename_dict)



## remove emptyspaces in Tags column between values
nf['Tags'] = nf['Tags'].str.replace(' ', '')

# Create an additional column 'Variant Inventory Tracker' with all values value 'shopify'
nf['Variant Inventory Tracker'] = 'shopify'
nf['Variant Inventory Policy'] = 'continue'
nf['Variant Fulfillment Service'] = 'manual'
nf['Variant Inventory Qty'] = '1'


# ### Save to google sheet

# In[90]:


import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe
import os
import dotenv
import json
from dotenv import load_dotenv

load_dotenv()

# Define the scope
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']

# Save the credentials to a JSON file if not already saved
CredentialsJson = {
    "type": os.getenv("TYPE"),
    "project_id": os.getenv("PROJECT_ID"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDgi/ULG3fwgxbi\npsWUpCwOkEjwAc7aSG4A2eCUTiC8nPEzM628EgjgQXN3Ef9rTqHQ8JNgUTDlzKqo\nnpQ+8JBYeH2s7YVG3IuytakS81vofjAGyTPRk7Cf3ih8TGicjam7kCDdL9FyFPIx\nQpABIKnWbdv4tV/Y/lIrvyCZ9+VH6B0SSK48yIh0nHvyq3EoUQZmbawiWf0m/FPS\n6lrX98xiyMpA9gYQ5eV8JH6iLBQgv8I1tAmheE64B/SufHgTQWAbJO9/uVOxo0Eh\nnfAt602BMyxCAVec1Ctoc6nXJFMwzTef/ppCC8c2jkIXE70zSPYffXtoCiBCfRP5\nZA7sO/jTAgMBAAECggEAGbNLJ6tMLgYC/4wQ/zNPK5eOEZJTZ550oLpPPwo2KwBX\nhwG6N9VkmK5FFfLEZjbIxI5Uf+irDRJA0i3cT9ve2ZFo6PsCjxq9DoZGRLn/4ftX\nad9rg+hAhfu6bIeeTZTVQXd8m3RWp5UIJ2Uz8D0Z00YdsDiqML7jDsjAZX7/Chyr\nGoY9Jo1aHq0VostiyAYPTYMhEMH+/OdeKVD+JysNSwrR7lEKCAPlrKAa58iRVawc\n8MMdhS+WjOit9Zx//X/ZgBvA3eubrwrxkFq8Uxsh5VtBnHk+6waidW5nW8Mlc8o3\nt6JrpPImwKtNbZcfrrBuGWJ+S4FJXshNUMeGb9aZGQKBgQD0QF+AmABEWxi9uDZv\n6SuxQS9UwCPtmvqZk+OorIFEOUApWRaMPMmpgy2xq8oVxyFRO/0z7JqQg1Pnqlyh\nriHzBk862H6SbxKhSCmWnJiAwEcFjvEFHHubf5ONIsiLE4rPfqJmMjjBtnFb9sOS\nNv2BSQtp+8y+OJB4x2L73C7gFQKBgQDrWPJeul5gJw6IwK9Psdur6ltMBcnQGtuR\nvwD6/r9QFd8lWtqVZxr7asqEegkVg+xe23lksiHWwvp2iEoaPjiucH78O4C7gRFE\n65EQKXzy5JT0BwaDkbuWW5ZDvf/vDrKa2cmTnCJ7zANvf4w5qtNUjuQ0pM4yFeFo\nnRsSvj5HRwKBgQCu/nft//khAEtnkdWetGYTZupsRAT5tTGaWrSfIoiywnnPpf5b\nlym8gzl3s+bjV3ntY5dzXi8XHqA8uHgJdmLoZTrapEV60I1+c98oAyXYCOpZdyID\nUXbV379tPOCFlAi9xLLBmXXEg9wP0WopFbDmsdi1pCv6lTgc8G1gmU4USQKBgBy5\nk4OKXcCAo95/Hias/7Hg/dmujy5OSORmGrmH5FPjB4RorWs01W9AXo2C058DphMB\n2LQ4pbavv6A+DEVduM9ZvbYNkS3RmAkAc4k0dyKyUZfjT6E5ZVr5vMJx604DTjtm\nP5s7oF3ZzcWLHNNhDUAx3JqsTtqAHy4EluxXugQ7AoGAUQe4xZjlRcsWLCgAc1UP\nfc8YsE0ctVpsYPb9c/Yzh7uVnrCHQ1QVD4aSf6TjGtRMnVgQXlR40y4S7Tg727x9\nlv+jYmK7RLKvWxgi5AIWQnz8QqWso/XsmFCmG+2XvLJ/jW+Vfcu27D0ROlQb4RKI\nV6YQkl6+DGwtHVECtRA68Bo=\n-----END PRIVATE KEY-----\n",
    "client_email": os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLIENT_ID"),
    "auth_uri": os.getenv("AUTH_URI"),
    "token_uri": os.getenv("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("UNIVERSE_DOMAIN")
}

# Save to a JSON file
with open('credentials.json', 'w') as json_file:
    json.dump(CredentialsJson, json_file)

# Authorize using the JSON file directly
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

# Authorize the clientsheet
client = gspread.authorize(creds)

# Open the Google Sheet (by name or by key)
spreadsheet = client.open("Fanatics_product_import")

# Select the first sheet (or specify another sheet)
sheet = spreadsheet.sheet1  

# Clear existing data in the sheet (optional)
sheet.clear()

# Write DataFrame to Google Sheet (ensure 'nf' is a valid DataFrame)
set_with_dataframe(sheet, nf)

