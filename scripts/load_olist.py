import pandas as pd
import sqlite3
import os


# database creation from raw data
#ETL (extract -> transform -> load)


print("Starting load script...") # Just to show starting booting system/ optional
print("Current folder:", os.getcwd()) # Show the current folder with the working directory in operating system

# Expected CSV files
csv_files = [
    "olist_orders_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_customers_dataset.csv",
    "olist_products_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_sellers_dataset.csv",
    "olist_geolocation_dataset.csv",
    "product_category_name_translation.csv"
]

db_file = "ecommerce.db" # we did this because python reads top to bottom and also as a  base to store the work in the script

print(f"\nDatabase will be saved as: {os.path.abspath(db_file)}") # prints a full path connection

conn = sqlite3.connect(db_file) # setting up sqlite 3 with working file
loaded_count = 0 # no new load had been done before it


for csv in csv_files: # better than to rewrite all the files name one by one
    if not os.path.exists(csv):  # security check if all files are working and present
        print(f" File not found in folder: {csv}") #if not then pass an error and the file name
        continue # move to next file repeat the process in loop until all file are checked



    try: # security check [some file can be corrupted or not present in the database this avoid the crashing the program]
        print(f"Reading {csv}...") #print the file and the text
        df = pd.read_csv(csv) # read that file
        # make a new table
        table_name = csv.replace("olist_", "").replace(".csv", "").replace("_dataset", "", )


        #df = raw data
        #to_sql = send df data to sql
        #table_name = the name of the table we just made
        #conn = sqlite3.connect(db_file) # this the connection we made at the top first
        #if exists = "replace" = if data exist overwrite it/ delete it and add new data
        #index= false = don't save as pandas indexing
        df.to_sql(table_name , conn, if_exists="replace", index=False)
        print(f"✓ Loaded successfully: {csv} → table '{table_name}' ({len(df):,} rows)") #print file table_name and length rows
        loaded_count += 1 # increment by 1


    except Exception as e: # throws an error
        print(f"Error loading {csv}: {e}")

conn.close() # if everything goes well close the connection now

print("\n" + "=" * 70) # make a line with = till 70 len
print(f"Load complete!") # print text
print(f"Successfully loaded {loaded_count} out of {len(csv_files)} files") # print text and load_count and len of csv
print(f"Database file size: {os.path.getsize(db_file) / (1024 * 1024):.2f} MB") # print text and path and size
print("If loaded 9 files and size > 30 MB → ready for analysis!") # print text
