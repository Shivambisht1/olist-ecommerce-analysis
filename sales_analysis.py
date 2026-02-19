import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to the database
conn = sqlite3.connect('ecommerce.db')

print("=== BASIC DATABASE CHECK ===")
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
print("Tables:", tables['name'].tolist())

print("\n=== ROW COUNTS ===")
for table in tables['name']:
    try:
        count = pd.read_sql(f"SELECT COUNT(*) FROM {table}", conn).iloc[0,0]
        print(f"{table:30} : {count:,} rows")
    except:
        print(f"{table:30} : ERROR")

print("\n=== ORDERS DATE RANGE ===")
date_range = pd.read_sql("""
    SELECT 
        MIN(order_purchase_timestamp) AS first_order,
        MAX(order_purchase_timestamp) AS last_order
    FROM orders;
""", conn)
print(date_range)

print("\n=== TOTAL REVENUE (BRL) ===")
revenue = pd.read_sql("""
    SELECT ROUND(SUM(payment_value), 2) AS total_revenue
    FROM order_payments;
""", conn)
print(revenue)

print("\n=== TOP 5 STATES BY CUSTOMERS ===")
top_states = pd.read_sql("""
    SELECT customer_state, COUNT(*) AS customer_count
    FROM customers
    GROUP BY customer_state
    ORDER BY customer_count DESC
    LIMIT 5;
""", conn)
print(top_states)

# ────────────────────────────────────────────────
# MAIN ANALYSIS SECTIONS

print("\n=== 1. MONTHLY REVENUE TREND ===")
monthly_revenue = pd.read_sql("""
    SELECT 
        STRFTIME('%Y-%m', order_purchase_timestamp) AS month,
        ROUND(SUM(payment_value), 2) AS revenue
    FROM orders o
    JOIN order_payments p ON o.order_id = p.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY month
    ORDER BY month;
""", conn)
print(monthly_revenue)

plt.figure(figsize=(12, 6))
plt.plot(monthly_revenue['month'], monthly_revenue['revenue'], marker='o', color='teal')
plt.title('Monthly Revenue Trend (Olist E-commerce)')
plt.xlabel('Month (YYYY-MM)')
plt.ylabel('Revenue (BRL)')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('monthly_revenue_trend.png')
plt.show()

print("\n=== 2. TOP 10 PRODUCT CATEGORIES BY REVENUE ===")
top_categories = pd.read_sql("""
    SELECT 
        pr.product_category_name,
        ROUND(SUM(i.price), 2) AS total_revenue,
        COUNT(DISTINCT i.order_id) AS num_orders
    FROM order_items i
    JOIN products pr ON i.product_id = pr.product_id
    GROUP BY pr.product_category_name
    ORDER BY total_revenue DESC
    LIMIT 10;
""", conn)
print(top_categories)

plt.figure(figsize=(10, 6))
sns.barplot(data=top_categories, x='total_revenue', y='product_category_name', hue='product_category_name', palette='viridis', legend=False)
plt.title('Top 10 Categories by Revenue')
plt.xlabel('Total Revenue (BRL)')
plt.ylabel('Category')
plt.tight_layout()
plt.savefig('top_categories.png')
plt.show()

print("\n=== 3. DELIVERY & DELAY ANALYSIS (Monthly) ===")
delivery_df = pd.read_sql("""
    SELECT 
        STRFTIME('%Y-%m', order_purchase_timestamp) AS month,
        ROUND(AVG(JULIANDAY(order_delivered_customer_date) - JULIANDAY(order_purchase_timestamp)), 2) AS avg_actual_days,
        ROUND(AVG(JULIANDAY(order_estimated_delivery_date) - JULIANDAY(order_purchase_timestamp)), 2) AS avg_estimated_days,
        SUM(CASE WHEN JULIANDAY(order_delivered_customer_date) > JULIANDAY(order_estimated_delivery_date) THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS late_delivery_pct,
        COUNT(*) AS delivered_orders
    FROM orders
    WHERE order_status = 'delivered'
      AND order_delivered_customer_date IS NOT NULL
      AND order_estimated_delivery_date IS NOT NULL
      AND order_purchase_timestamp IS NOT NULL
    GROUP BY month
    ORDER BY month;
""", conn)
print(delivery_df)

# Plot 1: Actual vs Estimated
plt.figure(figsize=(12, 6))
plt.plot(delivery_df['month'], delivery_df['avg_actual_days'], marker='o', label='Actual Days', color='orange')
plt.plot(delivery_df['month'], delivery_df['avg_estimated_days'], marker='s', label='Estimated Days', color='green', linestyle='--')
plt.title('Actual vs Estimated Delivery Time per Month')
plt.xlabel('Month (YYYY-MM)')
plt.ylabel('Days')
plt.legend()
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('delivery_performance.png')
plt.show()

# Plot 2: Late %
plt.figure(figsize=(10, 5))
sns.barplot(data=delivery_df, x='month', y='late_delivery_pct', color='salmon')
plt.title('Percentage of Late Deliveries per Month')
plt.xlabel('Month')
plt.ylabel('Late Deliveries (%)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('late_delivery_pct.png')
plt.show()

conn.close()

print("\nAll done! Check your folder for these images:")
print(" - monthly_revenue_trend.png")
print(" - top_categories.png")
print(" - delivery_performance.png")
print(" - late_delivery_pct.png")