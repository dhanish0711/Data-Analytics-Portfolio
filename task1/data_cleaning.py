import os
import pandas as pd
import numpy as np

# Define file paths
input_file = r"F:\Data Analytics Internship Portfolio\ApexPlanet_DataAnalytics_Dataset.xlsx"
output_dir = r"F:\Data Analytics Internship Portfolio\task1"
output_xlsx = os.path.join(output_dir, "cleaned_sales_dataset.xlsx")
output_csv = os.path.join(output_dir, "cleaned_sales_dataset.csv")

def main():
    print("Starting Data Wrangling and Cleaning process...")
    
    # 1. Load the dataset
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
        
    df = pd.read_excel(input_file, sheet_name="Sales_Dataset")
    print(f"Original dataset shape: {df.shape}")
    
    # Keep track of changes for documentation
    cleaning_summary = {}

    # 2. Handle Duplicate Order_ID Sequence Corruption
    # Mismatch formula check: expected is ORD(100002 + index)
    corrupted_indices = []
    for idx, row in df.iterrows():
        expected_id = f"ORD{100002 + idx}"
        if row["Order_ID"] != expected_id:
            corrupted_indices.append((idx, row["Order_ID"], expected_id))
            
    cleaning_summary["order_id_corrections"] = len(corrupted_indices)
    print(f"Found {len(corrupted_indices)} corrupted Order_ID entries.")
    
    for idx, old_id, new_id in corrupted_indices:
        df.at[idx, "Order_ID"] = new_id
        
    # 3. Impute Missing Values in 'Age'
    missing_ages = df["Age"].isnull().sum()
    cleaning_summary["missing_ages_imputed"] = missing_ages
    median_age = df["Age"].median()
    print(f"Imputing {missing_ages} missing Age values with overall median age: {median_age}")
    df["Age"] = df["Age"].fillna(median_age)
    
    # Convert Age to integer since ages are whole numbers
    df["Age"] = df["Age"].astype(int)

    # 4. Impute Missing Values in 'City'
    missing_cities = df["City"].isnull().sum()
    cleaning_summary["missing_cities_imputed"] = missing_cities
    print(f"Imputing {missing_cities} missing City values with 'Unknown'")
    df["City"] = df["City"].fillna("Unknown")

    # 5. Standardize Data Types
    print("Standardizing data types...")
    # Convert Order_Date to datetime
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], format="%Y-%m-%d")

    # 6. Feature Engineering
    print("Performing feature engineering...")
    # A. Age Group
    # Bins: 18-30 (Young Adult), 31-50 (Adult), 51-65 (Senior)
    age_bins = [17, 30, 50, 66]
    age_labels = ["Young Adult (18-30)", "Adult (31-50)", "Senior (51-65)"]
    df["Age_Group"] = pd.cut(df["Age"], bins=age_bins, labels=age_labels)

    # B. Date Parts
    df["Order_Year"] = df["Order_Date"].dt.year
    df["Order_Month"] = df["Order_Date"].dt.month
    df["Order_Day"] = df["Order_Date"].dt.day
    df["Order_DayOfWeek"] = df["Order_Date"].dt.day_name()
    
    # C. Is Weekend
    df["Is_Weekend"] = df["Order_DayOfWeek"].isin(["Saturday", "Sunday"])

    # 7. Verification Assertions (Data Quality Checks)
    print("\n--- Verifying Data Integrity ---")
    
    # Check for nulls
    nulls_remaining = df.isnull().sum().sum()
    print(f"Total null values remaining: {nulls_remaining}")
    assert nulls_remaining == 0, f"Error: {nulls_remaining} null values remaining in cleaned dataset!"

    # Check for duplicate Order_IDs
    dup_order_ids = df["Order_ID"].duplicated().sum()
    print(f"Duplicate Order_ID count: {dup_order_ids}")
    assert dup_order_ids == 0, f"Error: {dup_order_ids} duplicate Order_IDs remain!"

    # Check data types
    assert pd.api.types.is_integer_dtype(df["Age"]), "Error: Age is not of integer type!"
    assert pd.api.types.is_datetime64_any_dtype(df["Order_Date"]), "Error: Order_Date is not a datetime!"

    # Verify calculation of Total_Sales
    calc_mismatches = np.abs(df["Total_Sales"] - (df["Quantity"] * df["Unit_Price"])) > 0.01
    mismatch_count = calc_mismatches.sum()
    print(f"Total sales calculation mismatches: {mismatch_count}")
    assert mismatch_count == 0, f"Error: {mismatch_count} rows have mismatched total sales calculations!"

    print("All integrity checks passed successfully!")

    # 8. Save output files
    print(f"Saving cleaned dataset to Excel: {output_xlsx}")
    df.to_excel(output_xlsx, index=False, sheet_name="Cleaned_Sales_Dataset")
    
    print(f"Saving cleaned dataset to CSV: {output_csv}")
    df.to_csv(output_csv, index=False)

    print("\n--- Summary of Cleaning Operations ---")
    print(f"- Corrected Order_ID sequence corruptions: {cleaning_summary['order_id_corrections']}")
    print(f"- Imputed missing Ages: {cleaning_summary['missing_ages_imputed']}")
    print(f"- Imputed missing Cities: {cleaning_summary['missing_cities_imputed']}")
    print(f"- Standardized order date formatting and converted Age to integer.")
    print(f"- Created feature columns: 'Age_Group', 'Order_Year', 'Order_Month', 'Order_Day', 'Order_DayOfWeek', 'Is_Weekend'.")
    print(f"- Output shape: {df.shape}")
    print("Process completed successfully!")

if __name__ == "__main__":
    main()
