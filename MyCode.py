import pandas as pd
import sqlite3

# Step 1: Load and Explore the Dataset
# Using a sample dataset for sales analysis.
data = {
    "OrderID": [1, 2, 3, 4, 5, 6],
    "CustomerID": [101, 102, 101, 103, 102, 104],
    "OrderDate": [
        "2023-12-01", "2023-12-02", "2023-12-03",
        "2023-12-03", "2023-12-04", "2023-12-05"
    ],
    "Product": ["Laptop", "Phone", "Tablet", "Laptop", "Tablet", "Phone"],
    "Quantity": [1, 2, 1, 1, 3, 2],
    "Price": [1000, 500, 300, 1200, 300, 550]
}

# Create a Pandas DataFrame
df = pd.DataFrame(data)
print("Initial Dataset:")
print(df)

# Step 2: Clean the Data
# Ensure data types are correct
df['OrderDate'] = pd.to_datetime(df['OrderDate'])
df['Revenue'] = df['Quantity'] * df['Price']
print("\nDataset after adding Revenue column:")
print(df)

# Step 3: Save Dataset to SQLite Database
conn = sqlite3.connect("sales_data.db")

df.to_sql("sales", conn, if_exists="replace", index=False)
print("\nData saved to SQLite database.")

# Step 4: Analyze Data Using SQL
# SQL Query 1: Total revenue
query1 = """
SELECT SUM(Revenue) as TotalRevenue FROM sales;
"""
total_revenue = pd.read_sql_query(query1, conn)
print("\nTotal Revenue:")
print(total_revenue)

# SQL Query 2: Top-selling products
query2 = """
SELECT Product, SUM(Quantity) as TotalQuantity
FROM sales
GROUP BY Product
ORDER BY TotalQuantity DESC;
"""
top_products = pd.read_sql_query(query2, conn)
print("\nTop-Selling Products:")
print(top_products)

# SQL Query 3: Revenue by Customer
query3 = """
SELECT CustomerID, SUM(Revenue) as TotalSpent
FROM sales
GROUP BY CustomerID
ORDER BY TotalSpent DESC;
"""
customer_revenue = pd.read_sql_query(query3, conn)
print("\nRevenue by Customer:")
print(customer_revenue)

# Step 5: Generate Insights
print("\nInsights:")
print(f"1. Total Revenue: {total_revenue.iloc[0]['TotalRevenue']}")
print(f"2. Top-Selling Product: {top_products.iloc[0]['Product']} with {top_products.iloc[0]['TotalQuantity']} units sold.")
print("3. Top Customers:")
print(customer_revenue.head())

# Step 6: Save Insights to a CSV File
output_file = "insights.csv"
customer_revenue.to_csv(output_file, index=False)
print(f"\nCustomer revenue insights saved to {output_file}.")

# Step 7: Close Database Connection
conn.close()
print("\nDatabase connection closed.")
