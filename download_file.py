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
