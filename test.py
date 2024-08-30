import pandas as pd
import os

# Get the current working directory
directory = os.getcwd()

# Path to the decompressed .txt file
local_txt_filename = os.path.join(directory, "Fanatics-Product-Catalog_IR.txt")

# Load the decompressed .txt file into a Pandas DataFrame
if os.path.exists(local_txt_filename):
    # Assuming the file is tab-delimited, adjust the delimiter if necessary
    df = pd.read_csv(local_txt_filename, delimiter='\t')
    print(df.head())  # Display the first 5 rows
else:
    print(f"{local_txt_filename} does not exist.")