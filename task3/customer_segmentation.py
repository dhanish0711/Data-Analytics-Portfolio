import os
import pandas as pd
import numpy as np

# File paths
input_file = r"F:\Data Analytics Internship Portfolio\task1\cleaned_sales_dataset.xlsx"
output_dir = r"F:\Data Analytics Internship Portfolio\task3"
customer_output_file = os.path.join(output_dir, "segmented_customers.csv")
dashboard_data_file = os.path.join(output_dir, "dashboard", "sales_data.js")

def main():
    print("Starting RFM Customer Segmentation...")
    
    # 1. Load the cleaned dataset
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Cleaned dataset not found: {input_file}")
    df = pd.read_excel(input_file)
    
    # Ensure date is parsed
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    
    # Reference date is set to 1 day after the max order date in the dataset
    ref_date = pd.to_datetime("2026-01-02")
    
    # 2. Group by Customer_ID to calculate Recency, Frequency, and Monetary (RFM)
    # Note: Since some Customer_IDs had multiple names/cities in raw data, we will:
    # - Group by Customer_ID
    # - Recency: Days since last order date relative to ref_date
    # - Frequency: Count of orders
    # - Monetary: Sum of Total_Sales
    # - Customer profile details (Name, Age, Gender, City): Take the most recent order's values
    
    # Find the index of the most recent order for each customer to extract their latest profile info
    latest_order_indices = df.sort_values('Order_Date').groupby('Customer_ID').tail(1).index
    customer_profiles = df.loc[latest_order_indices, ['Customer_ID', 'Customer_Name', 'Age', 'Gender', 'City']].set_index('Customer_ID')
    
    # Calculate RFM metrics
    rfm = df.groupby('Customer_ID').agg(
        Last_Order_Date=('Order_Date', 'max'),
        Frequency=('Order_ID', 'count'),
        Monetary=('Total_Sales', 'sum')
    )
    
    rfm['Recency'] = (ref_date - rfm['Last_Order_Date']).dt.days
    
    # Join with profiles
    rfm_profiles = rfm.join(customer_profiles)
    
    # 3. Assign RFM Scores from 1 to 5
    # Recency: Lower is better (more recent). Quantiles from 1 to 5 (5 is most recent, 1 is oldest)
    # Using duplicates='drop' or custom bins because of potential tie values
    rfm_profiles['R_Score'] = pd.qcut(rfm_profiles['Recency'], q=5, labels=[5, 4, 3, 2, 1]).astype(int)
    
    # Frequency: Higher is better. Since frequency is almost all 1 or 2, we map scores:
    # 1 -> 1, 2 -> 3, >=3 -> 5
    def get_f_score(freq):
        if freq == 1:
            return 1
        elif freq == 2:
            return 3
        else:
            return 5
    rfm_profiles['F_Score'] = rfm_profiles['Frequency'].apply(get_f_score)
    
    # Monetary: Higher is better. Quantiles from 1 to 5 (5 is highest spend, 1 is lowest)
    rfm_profiles['M_Score'] = pd.qcut(rfm_profiles['Monetary'], q=5, labels=[1, 2, 3, 4, 5]).astype(int)
    
    # 4. Segment Customers based on R, F, M Scores
    def segment_customer(row):
        r = row['R_Score']
        f = row['F_Score']
        m = row['M_Score']
        
        # Champions: Recent, frequent, and high spenders
        if r >= 4 and m >= 4:
            return "Champions"
        # Loyal Customers: Good recency and frequency or monetary
        elif r >= 3 and (f >= 3 or m >= 3):
            return "Loyal Customers"
        # New Customers: Recent but low spend/frequency
        elif r >= 4 and f == 1 and m <= 2:
            return "New Customers"
        # At Risk: High spend in the past, but inactive
        elif r <= 2 and m >= 4:
            return "At Risk"
        # Lost / Low-Value: Inactive, low spend
        elif r <= 2 and m <= 2:
            return "Lost / Low-Value"
        # Default category
        else:
            return "Average Spenders"
            
    rfm_profiles['RFM_Segment'] = rfm_profiles.apply(segment_customer, axis=1)
    
    # Save customer profiles
    os.makedirs(output_dir, exist_ok=True)
    rfm_profiles.to_csv(customer_output_file)
    print(f"Customer profiles with segments saved to: {customer_output_file}")
    
    # 5. Merge segments back to the main transactions dataframe for the dashboard
    segment_mapping = rfm_profiles['RFM_Segment'].to_dict()
    df['RFM_Segment'] = df['Customer_ID'].map(segment_mapping)
    
    # Check segment counts
    print("\n--- Segment Counts ---")
    print(df['RFM_Segment'].value_counts())
    
    # 6. Output sales transactions as a javascript file for the frontend
    # Convert dates to string format
    df_js = df.copy()
    df_js['Order_Date'] = df_js['Order_Date'].dt.strftime('%Y-%m-%d')
    
    # Ensure target folder exists
    os.makedirs(os.path.dirname(dashboard_data_file), exist_ok=True)
    
    # Write to sales_data.js
    json_data = df_js.to_json(orient='records')
    js_content = f"// Automatically generated sales transactions with RFM segments\nconst salesData = {json_data};\n"
    
    with open(dashboard_data_file, 'w', encoding='utf-8') as f:
        f.write(js_content)
        
    print(f"Javascript dataset for dashboard written to: {dashboard_data_file}")
    print("RFM Customer Segmentation completed successfully!")

if __name__ == "__main__":
    main()
