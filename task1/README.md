# Task 1: Data Immersion & Wrangling

## Objective
To rapidly get acquainted with the raw sales transactions dataset, perform a thorough data quality assessment to identify issues, clean the data using a reproducible Python/Pandas pipeline, and prepare a final, analysis-ready dataset.

---

## 1. Data Dictionary

The cleaned dataset contains **1,000 rows** and **18 columns** representing individual sales transactions. Below is the documentation of all variables:

| Column Name | Data Type (Raw) | Data Type (Cleaned) | Description | Example Values | Business Relevance |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Order_ID** | String (Object) | String (Object) | Unique identifier for each transaction sequence. | `ORD100002`, `ORD100120` | Primary key for tracking individual sales transactions. |
| **Order_Date** | String (Object) | Datetime | Date the transaction took place. | `2025-02-25` | Necessary for time-series analysis, seasonality, and cohort tracking. |
| **Customer_ID** | String (Object) | String (Object) | Unique identifier for each customer. | `CUST5529`, `CUST3127` | Helps track customer behavior, repeat purchases, and customer lifetime value. |
| **Customer_Name**| String (Object) | String (Object) | Masked name of the customer. | `Customer_227`, `Customer_71` | Identifies individual customers while preserving privacy. |
| **Age** | Float | Integer | Age of the customer in years. | `41`, `18`, `65` | Demographic analysis, market segmentation, and targeting. |
| **Gender** | String (Object) | String (Object) | Gender of the customer. | `Male`, `Female` | Demographic profiling and product preference analysis. |
| **City** | String (Object) | String (Object) | City where the customer is located. | `Bengaluru`, `Patna`, `Unknown` | Geographical analysis and sales distribution. |
| **Product** | String (Object) | String (Object) | Specific item purchased. | `Rice`, `Laptop`, `Chair` | Product performance analysis and inventory planning. |
| **Category** | String (Object) | String (Object) | General category of the product. | `Electronics`, `Grocery` | High-level sales categorization and inventory planning. |
| **Quantity** | Integer | Integer | Number of units purchased. | `7`, `1`, `10` | Volume tracking, basket size, and bulk purchase behavior. |
| **Unit_Price** | Float | Float | Price per single unit of the product. | `2829.77`, `145.78` | Pricing strategy, margin analysis, and price elasticity. |
| **Total_Sales** | Float | Float | Total transaction value (`Quantity * Unit_Price`). | `19808.39`, `1762.62` | Revenue tracking, total sales value, and profitability. |
| **Age_Group** | - | Categorical | Age category of the customer. | `Adult (31-50)`, `Young Adult (18-30)` | Simplifies demographic segmentation for reporting. |
| **Order_Year** | - | Integer | Year component extracted from Order_Date. | `2025`, `2026` | Yearly revenue trends and reporting. |
| **Order_Month** | - | Integer | Month component extracted from Order_Date. | `2`, `10` | Monthly seasonality analysis. |
| **Order_Day** | - | Integer | Day of month extracted from Order_Date. | `25`, `14` | Daily sales analysis. |
| **Order_DayOfWeek**| - | String (Object) | Day name extracted from Order_Date. | `Tuesday`, `Saturday` | Weekly performance analysis (weekday vs weekend). |
| **Is_Weekend** | - | Boolean | Flag indicating if transaction occurred on a weekend. | `True`, `False` | Analyzes differences in weekend vs. weekday purchase patterns. |

---

## 2. Data Quality Assessment (DQA)

Prior to cleaning, the dataset was profiled, and the following critical issues were identified:

1. **Duplicate Order_ID Sequence Corruption:**
   - **Issue:** 8 transactions had duplicate `Order_ID` values. Specifically, `ORD100050` was reused 9 times in total.
   - **Analysis:** By examining the surrounding rows of these duplicates, we discovered that they were not duplicate rows (they had completely different customer IDs, dates, quantities, and prices). Instead, there was a sequential sequence corruption:
     - Row 118 was recorded as `ORD100050` instead of `ORD100120`.
     - Row 238 was recorded as `ORD100050` instead of `ORD100240`.
     - (This pattern was consistent for indices 118, 238, 358, 478, 598, 718, 838, and 958).
   - **Impact:** Compromises data integrity since `Order_ID` is supposed to be unique.

2. **Missing Values in Age:**
   - **Issue:** 20 customer records had missing `Age` values.
   - **Impact:** Hampers demographic and customer profiling.

3. **Missing Values in City:**
   - **Issue:** 13 transaction records had missing `City` values.
   - **Impact:** Skews geographic analysis.

4. **Inconsistent Data Types:**
   - **Issue:** `Order_Date` was formatted as a string (object). `Age` was recorded as a float instead of integer.

---

## 3. Cleaning & Transformation Logic

The cleaning pipeline in [data_cleaning.py](file:///f:/Data%20Analytics%20Internship%20Portfolio/task1/data_cleaning.py) implements the following steps:

1. **Reconstruct Corrupted Order_ID Sequence:**
   - The sequence formula `ORD(100002 + index)` was used to programmatically repair the 8 corrupted `Order_ID` values that had been mistakenly set to `ORD100050`. This restored uniqueness without discarding valid transaction data.
2. **Impute Missing Age Values:**
   - Missing ages were filled with the overall dataset median age (`41.0`).
   - The column was then cast to a 32-bit Integer (`int`).
3. **Impute Missing City Values:**
   - Missing cities were filled with the category `"Unknown"` to avoid making false assumptions about customer locations.
4. **Standardize Date Column:**
   - `Order_Date` was parsed and converted to Pandas `datetime` format.
5. **Verify Product and Category mapping:**
   - Cross-tabulation showed perfect category-to-product mapping (e.g. `Laptop` and `Mobile` always map to `Electronics`; `Book` to `Education`, etc.).
6. **Total Sales Mathematical Validation:**
   - Confirmed that `Total_Sales` is mathematically equal to `Quantity * Unit_Price` across all 1,000 rows.

---

## 4. Feature Engineering

To enrich the dataset for future exploratory analysis, we engineered the following features:
- **Age_Group:** Binned age into three main demographic segments:
  - `Young Adult (18-30)`
  - `Adult (31-50)`
  - `Senior (51-65)`
- **Date Parts (`Order_Year`, `Order_Month`, `Order_Day`):** Extracted integer parts from `Order_Date` for time-series aggregation.
- **Order_DayOfWeek:** Extracted the weekday name (e.g. `Monday`, `Tuesday`).
- **Is_Weekend:** A boolean flag representing whether the order was placed on a weekend (`Saturday` or `Sunday`).

---

## 5. Output Deliverables
The cleaned and enriched outputs are exported as:
- **CSV Format:** [cleaned_sales_dataset.csv](file:///f:/Data%20Analytics%20Internship%20Portfolio/task1/cleaned_sales_dataset.csv)
- **Excel Format:** [cleaned_sales_dataset.xlsx](file:///f:/Data%20Analytics%20Internship%20Portfolio/task1/cleaned_sales_dataset.xlsx)
- **Cleaning Script:** [data_cleaning.py](file:///f:/Data%20Analytics%20Internship%20Portfolio/task1/data_cleaning.py)

---
*Created as part of Task 1 for the Data Analytics Internship Portfolio.*
