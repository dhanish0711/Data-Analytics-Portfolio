import os
import sqlite3
import pandas as pd

# File paths
input_file = r"F:\Data Analytics Internship Portfolio\task1\cleaned_sales_dataset.xlsx"
db_file = r"F:\Data Analytics Internship Portfolio\task2\task2_database.db"
output_log = r"F:\Data Analytics Internship Portfolio\task2\sql_queries_output.txt"

def setup_database():
    print("Setting up SQLite database...")
    # Delete old database if exists
    if os.path.exists(db_file):
        os.remove(db_file)
        
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("""
    CREATE TABLE products (
        Product_Name TEXT PRIMARY KEY,
        Category TEXT NOT NULL
    );
    """)
    
    cursor.execute("""
    CREATE TABLE regions (
        City TEXT PRIMARY KEY,
        Region TEXT NOT NULL
    );
    """)
    
    cursor.execute("""
    CREATE TABLE sales (
        Order_ID TEXT PRIMARY KEY,
        Order_Date TEXT NOT NULL,
        Customer_ID TEXT NOT NULL,
        Customer_Name TEXT NOT NULL,
        Age INTEGER NOT NULL,
        Gender TEXT NOT NULL,
        City TEXT NOT NULL,
        Product TEXT NOT NULL,
        Quantity INTEGER NOT NULL,
        Unit_Price REAL NOT NULL,
        Total_Sales REAL NOT NULL,
        FOREIGN KEY (Product) REFERENCES products (Product_Name),
        FOREIGN KEY (City) REFERENCES regions (City)
    );
    """)
    
    conn.commit()
    conn.close()
    print("Database schema created successfully.")

def populate_database():
    print("Populating SQLite tables from cleaned dataset...")
    df = pd.read_excel(input_file)
    
    conn = sqlite3.connect(db_file)
    
    # 1. Populate products table
    # Unique product name and category
    products_df = df[['Product', 'Category']].drop_duplicates().rename(columns={'Product': 'Product_Name'})
    products_df.to_sql('products', conn, if_exists='append', index=False)
    
    # 2. Populate regions table
    # Map cities to regions
    unique_cities = df['City'].unique()
    region_mapping = {
        'Bengaluru': 'South',
        'Delhi': 'North',
        'Gaya': 'East',
        'Hyderabad': 'South',
        'Kolkata': 'East',
        'Mumbai': 'West',
        'Patna': 'East',
        'Pune': 'West',
        'Unknown': 'Unknown'
    }
    regions_data = [{'City': city, 'Region': region_mapping.get(city, 'Unknown')} for city in unique_cities]
    regions_df = pd.DataFrame(regions_data)
    regions_df.to_sql('regions', conn, if_exists='append', index=False)
    
    # 3. Populate sales table
    sales_df = df[[
        'Order_ID', 'Order_Date', 'Customer_ID', 'Customer_Name',
        'Age', 'Gender', 'City', 'Product', 'Quantity', 'Unit_Price', 'Total_Sales'
    ]]
    # Convert Order_Date to string format for SQLite
    sales_df = sales_df.copy()
    sales_df['Order_Date'] = sales_df['Order_Date'].dt.strftime('%Y-%m-%d')
    sales_df.to_sql('sales', conn, if_exists='append', index=False)
    
    conn.commit()
    
    # Verify counts
    cursor = conn.cursor()
    print("Populated row counts:")
    for table in ['products', 'regions', 'sales']:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        print(f"- {table}: {cursor.fetchone()[0]}")
        
    conn.close()

def run_queries():
    print("Executing SQL Business Questions...")
    conn = sqlite3.connect(db_file)
    
    queries = {
        "Q1_Category_Performance": {
            "title": "Question 1: Total Revenue and Sales Volume by Product Category",
            "desc": "Show total sales revenue and total quantity sold for each product category, ordered by revenue descending.",
            "sql": """
SELECT 
    p.Category,
    ROUND(SUM(s.Total_Sales), 2) AS Total_Revenue_INR,
    SUM(s.Quantity) AS Total_Quantity_Sold,
    COUNT(s.Order_ID) AS Total_Orders
FROM sales s
JOIN products p ON s.Product = p.Product_Name
GROUP BY p.Category
ORDER BY Total_Revenue_INR DESC;
"""
        },
        "Q2_Electronics_Top_Products": {
            "title": "Question 2: Top Performing Products within the Electronics Category",
            "desc": "Find the top performing products by total sales revenue within the 'Electronics' category.",
            "sql": """
SELECT 
    s.Product,
    p.Category,
    ROUND(SUM(s.Total_Sales), 2) AS Total_Revenue_INR,
    SUM(s.Quantity) AS Total_Quantity_Sold,
    ROUND(AVG(s.Unit_Price), 2) AS Avg_Unit_Price_INR
FROM sales s
JOIN products p ON s.Product = p.Product_Name
WHERE p.Category = 'Electronics'
GROUP BY s.Product
ORDER BY Total_Revenue_INR DESC;
"""
        },
        "Q3_Monthly_Sales_Trend": {
            "title": "Question 3: Monthly Sales Revenue and Order Count Trends (2025)",
            "desc": "Analyze monthly sales performance and transaction volumes for the year 2025.",
            "sql": """
SELECT 
    strftime('%Y-%m', Order_Date) AS Month,
    ROUND(SUM(Total_Sales), 2) AS Monthly_Revenue_INR,
    COUNT(Order_ID) AS Order_Count,
    SUM(Quantity) AS Total_Quantity_Sold
FROM sales
WHERE Order_Date BETWEEN '2025-01-01' AND '2025-12-31'
GROUP BY Month
ORDER BY Month ASC;
"""
        },
        "Q4_Geographical_Revenue_Region": {
            "title": "Question 4: Geographical Sales Performance by City and Region",
            "desc": "Calculate total revenue, order count, and average order value (AOV) for each city and its region using a multi-table join.",
            "sql": """
SELECT 
    s.City,
    r.Region,
    ROUND(SUM(s.Total_Sales), 2) AS Total_Revenue_INR,
    COUNT(s.Order_ID) AS Order_Count,
    ROUND(AVG(s.Total_Sales), 2) AS Average_Order_Value_INR
FROM sales s
JOIN regions r ON s.City = r.City
GROUP BY s.City, r.Region
ORDER BY Total_Revenue_INR DESC;
"""
        },
        "Q5_High_Value_Customers": {
            "title": "Question 5: Top 5 High-Value Customers by Revenue",
            "desc": "Identify the top 5 customers who spent the most money and show their order count and average transaction size.",
            "sql": """
SELECT 
    Customer_ID,
    Customer_Name,
    ROUND(SUM(Total_Sales), 2) AS Total_Spend_INR,
    COUNT(Order_ID) AS Order_Count,
    ROUND(AVG(Total_Sales), 2) AS Avg_Order_Size_INR
FROM sales
GROUP BY Customer_ID, Customer_Name
ORDER BY Total_Spend_INR DESC
LIMIT 5;
"""
        },
        "Q6_Weekday_Weekend_Comparison": {
            "title": "Question 6: Weekday vs. Weekend Sales Performance Comparison",
            "desc": "Compare total revenue, total quantity, and average order size between weekdays and weekends.",
            "sql": """
SELECT 
    CASE 
        -- strftime('%w', Order_Date) returns '0' for Sunday and '6' for Saturday
        WHEN strftime('%w', Order_Date) IN ('0', '6') THEN 'Weekend'
        ELSE 'Weekday'
    END AS Day_Type,
    ROUND(SUM(Total_Sales), 2) AS Total_Revenue_INR,
    SUM(Quantity) AS Total_Quantity_Sold,
    COUNT(Order_ID) AS Order_Count,
    ROUND(AVG(Total_Sales), 2) AS Average_Order_Value_INR
FROM sales
GROUP BY Day_Type;
"""
        }
    }

    # Execute and format results to log
    with open(output_log, 'w', encoding='utf-8') as f:
        f.write("=== SQL BUSINESS QUESTIONS & QUERY RESULTS ===\n\n")
        
        for q_id, q_info in queries.items():
            print(f"Running: {q_info['title']}...")
            f.write(f"### {q_info['title']}\n")
            f.write(f"**Description:** {q_info['desc']}\n\n")
            f.write("```sql\n" + q_info['sql'].strip() + "\n```\n\n")
            
            # Execute query using pandas for pretty markdown table formatting
            res_df = pd.read_sql_query(q_info['sql'], conn)
            
            f.write("**Result Set:**\n\n")
            f.write(res_df.to_markdown(index=False))
            f.write("\n\n" + "="*80 + "\n\n")
            
    conn.close()
    print(f"All query results successfully logged to: {output_log}")

def main():
    setup_database()
    populate_database()
    run_queries()

if __name__ == "__main__":
    main()
