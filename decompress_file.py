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
