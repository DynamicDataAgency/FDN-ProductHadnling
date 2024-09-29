import pandas as pd
import os

# Get the current working directory
directory = os.path.join(os.getcwd(), "data-update-process")

# Path to the decompressed .txt file
local_txt_filename = os.path.join(directory, "Fanatics-Product-Catalog_IR.txt")

# Load the decompressed .txt file into a Pandas DataFrame
if os.path.exists(local_txt_filename):
    # Assuming the file is tab-delimited, adjust the delimiter if necessary
    df = pd.read_csv(local_txt_filename, delimiter='\t', low_memory=False)
    print(df.head())  # Display the first 5 rows

    # Filter needed products
    df = df[df["Category"] == "NFL"]
    df = df.head(2000)

    # Transformations to fit Shopify product import
    nf = df.loc[:, ['Unique Merchant SKU', 'Product Name', 'Product URL', 'Image URL', 'Current Price', 
                    'Original Price', 'Product Description', 'Gender', 'Text1', 'Text2', 'Text3','Size']]

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
    nf['Tags'] = nf['Tags'].str.replace(' ', '')  # Remove empty spaces in Tags column
    nf['Variant Inventory Tracker'] = 'shopify'
    nf['Variant Inventory Policy'] = 'continue'
    nf['Variant Fulfillment Service'] = 'manual'
    nf['Variant Inventory Qty'] = '1'

    # Save the DataFrame for the next step
    nf.to_csv('processed_data.csv', index=False)  # Save the DataFrame to a CSV file
else:
    print(f"{local_txt_filename} does not exist.")
