import sqlite3
import pandas as pd

# using our previous database (e-commerce)
# This is EDA (Exploratory Data Analysis)
# we ask the insight for the database

#=== KEY POINTS ===
#CONNECTION
#PRINT TABLE (TXT)
#SQL QUEARY  (Gets all table names in the database)
# PRINT TABLE OUTPUT
# PRINT ROW_COUNTS (TXT)
# EMPTY DICT
# LOOP TABLE
# SECURITY CHECK
# QUERY = PANDAS = EXTRACT NUMBER
# STORE INTO EMPTY DICT
# CLEAN FORMAT


# MORE COMING


# Connect to the database
conn = sqlite3.connect('ecommerce.db') #    #CONNECTION

# 1. List all tables to confirm
print("=== TABLES IN DATABASE ===") # PRINT
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn) # TABLES READ
print(tables) # PRINT TABLE


print("\n=== ROW COUNTS ===") # just plain text
row_counts = {} # EMPTY DICT
for table in tables['name']: # FILE CHECK


    try: # security check
        count = pd.read_sql(f"SELECT COUNT(*) FROM {table}", conn).iloc[0,0] #
        row_counts[table] = count #
        print(f"{table:50} : {count:,} rows")
    except:
        print(f"{table:40} : ERROR")



    ## === PART TWO=== ###

# 3. Date range of orders (very important for time-based analysis)
print("\n=== ORDERS DATE RANGE ===")
date_range = pd.read_sql("""
    SELECT 
        MIN(order_purchase_timestamp) AS first_order,
        MAX(order_purchase_timestamp) AS last_order
    FROM orders;
""", conn)
print(date_range)

# 4. Total revenue
print("\n=== TOTAL REVENUE (BRL) ===")
revenue = pd.read_sql("""
    SELECT ROUND(SUM(payment_value), 2) AS total_revenue
    FROM order_payments;
""", conn)
print(revenue)

# 5. Top 5 states by number of customers
print("\n=== TOP 5 STATES BY CUSTOMERS ===")
top_states = pd.read_sql("""
    SELECT 
        customer_state,
        COUNT(*) AS customer_count
    FROM customers
    GROUP BY customer_state
    ORDER BY customer_count DESC
    LIMIT 5;
""", conn)
print(top_states)

conn.close()

