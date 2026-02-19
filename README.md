# Olist E-commerce Sales & Delivery Analysis

SQL + Pandas analysis of ~100,000 real Brazilian e-commerce orders (Olist public dataset, 2016–2018).

### What I Built
- ETL pipeline to load CSVs into SQLite database (`load_olist.py`)
- Basic data exploration & validation (`explore.py`)
- Full EDA & business analysis (`sales_analysis.py`):
  - Monthly revenue trends (peak in Nov 2017)
  - Top product categories (Health & Beauty leading)
  - Delivery performance: actual vs estimated time + late delivery percentage

### Visualizations
- monthly_revenue_trend.png
- top_categories.png
- delivery_performance.png
- late_delivery_pct.png

### Key Insights
- Total revenue: ~16 million BRL
- Top categories: beleza_saude (1.26M BRL), relogios_presentes (1.21M BRL)
- Delivery: actual 8–15 days, late rate 5–15% in many months

### Recommendations
- Focus marketing on Health & Beauty and Watches/Gifts
- Strengthen logistics during Nov–Dec peaks
- Improve delivery estimates to reduce dissatisfaction

### Tools
- Python (Pandas, Matplotlib, Seaborn)
- SQL (SQLite: joins, STRFTIME, JULIANDAY, CASE)
- GitHub

Data source: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Shivam Bisht  
Dehradun, India
