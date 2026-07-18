# Task 3: Deep-Dive Analysis & Interactive Dashboarding

## Objective
To answer complex business questions by performing a deep-dive **RFM (Recency, Frequency, Monetary) Customer Segmentation Analysis** and building a fully interactive, automated dashboard that surfaces core KPIs and allows business stakeholders to explore customer behavioral insights in real-time.

---

## 1. Core KPI Definitions

We have formally defined **5 Key Performance Indicators (KPIs)** to monitor sales health and customer engagement:

1. **Total Sales Revenue**
   - **Formula:** $\sum \text{Total\_Sales}$
   - **Business Rationale:** The primary top-line growth metric. It tracks the cumulative transaction volume across categories, channels, and locations, indicating overall business size.

2. **Total Transactions (Orders)**
   - **Formula:** $\text{Count of unique } \text{Order\_ID}$
   - **Business Rationale:** Tracks order volume and operational throughput. Increasing transaction counts with flat revenue implies order value is dropping, while decreasing transaction counts with high revenue implies order value is growing (fewer but larger orders).

3. **Average Order Value (AOV)**
   - **Formula:** $\frac{\text{Total Sales Revenue}}{\text{Total Transactions}}$
   - **Business Rationale:** Monitors buying efficiency. Increasing AOV is a cost-effective way to grow revenue since it doesn't require acquiring new customers; it can be driven by cross-selling, upselling, or volume discounts.

4. **Active Customer Count**
   - **Formula:** $\text{Count of unique } \text{Customer\_ID}$
   - **Business Rationale:** Measures customer base size and retention. A growing customer count represents successful acquisition, whereas a stable/increasing customer base with growing transaction frequency represents strong retention.

5. **Weekend Sales Share (%)**
   - **Formula:** $\frac{\text{Weekend Sales Revenue}}{\text{Total Sales Revenue}} \times 100\%$
   - **Business Rationale:** Identifies weekend vs. weekday shopping patterns. This metric helps allocate marketing budgets and ad spend (e.g. promoting high-value categories like electronics on weekends when buyers have more leisure time).

---

## 2. Customer RFM Segmentation Analysis

Since **94.5%** of the customer base made exactly one purchase in the dataset, traditional equal-frequency binning for Frequency was replaced by custom business-ruled scoring.

### Scoring Methodology
* **Recency (R) Score (1 to 5):** Calculated using days since last purchase relative to the reference date `2026-01-02`. Grouped into quintiles: Score 5 represents the most recent buyers (0-72 days), while Score 1 represents customers who haven't purchased in over 290 days.
* **Frequency (F) Score (1 to 5):** Assigned via business rules:
  - 1 Purchase $\rightarrow$ Score 1
  - 2 Purchases $\rightarrow$ Score 3
  - $\ge 3$ Purchases $\rightarrow$ Score 5
* **Monetary (M) Score (1 to 5):** Calculated based on total customer lifetime spend. Grouped into quintiles: Score 5 represents the top 20% spenders (above ₹240K), and Score 1 represents the lowest 20% spenders (below ₹20K).

### Customer Segment Breakdown
Applying combined RFM scores classifies our **947 unique customers** into 6 distinct behavioral segments:

| RFM Segment | Customer Count | Transaction Share | Description | Business Rationale & Action Plan |
| :--- | :---: | :---: | :--- | :--- |
| **Loyal Customers** | 199 | 19.9% | Moderate-to-high frequency and monetary scores; buy regularly. | **Action Plan:** Target with loyalty programs, solicit product reviews, and cross-sell items. |
| **Champions** | 197 | 19.7% | Bought recently, buy often, and spend the most (high R and M). | **Action Plan:** Focus on retention. Offer early access to new products, VIP rewards, and personalized appreciation. |
| **Average Spenders** | 161 | 16.1% | Average scores across all three RFM dimensions. | **Action Plan:** Encourage repeat buying through personalized recommendations and bundle deals to increase AOV. |
| **Lost / Low-Value** | 157 | 15.7% | Haven't bought in a long time; low purchase frequency and low spend. | **Action Plan:** Low priority. Avoid expensive marketing; run low-cost email reactivation campaigns. |
| **At Risk** | 152 | 15.2% | High spenders in the past who haven't purchased in a long time. | **Action Plan:** High priority reactivation. Send personalized "We miss you" offers, surveys to resolve issues, and high-discount vouchers. |
| **New Customers** | 134 | 13.4% | Made their first purchase very recently (high R, low F and M). | **Action Plan:** Trigger welcome emails, onboarding sequences, and post-purchase follow-ups with discounts for a second purchase. |

*Detailed customer metrics are saved in the generated file: [segmented_customers.csv](file:///f:/Data%20Analytics%20Internship%20Portfolio/task3/segmented_customers.csv).*

---

## 3. Interactive BI Dashboard

We built a custom, client-side interactive BI dashboard web application in [task3/dashboard/](file:///f:/Data%20Analytics%20Internship%20Portfolio/task3/dashboard/).

### Dashboard Features
- **Dynamic KPI Metrics:** Total Revenue, Total Orders, AOV, Customers, and Weekend Sales Share update instantly based on chosen filters.
- **Global Dropdown Filters:** Users can filter all visuals by **City, Category, Customer RFM Segment, Gender, and Age Group** simultaneously.
- **Interactive Visualizations:**
  - **Monthly Sales Trend (Line Chart):** Displays revenue changes over time.
  - **Category Share (Donut Chart):** Shows revenue distribution across categories (with tooltips indicating percentage).
  - **RFM Segments (Bar Chart):** Displays customer counts in each segment.
- **Top 10 High-Value Customers (Data Table):** Dynamically ranks and renders the top 10 customers based on selected filters, showing their ID, Name, City, Orders, Segment, and Total Spend.

### How to Run Locally
1. Navigate to the dashboard directory: [task3/dashboard/](file:///f:/Data%20Analytics%20Internship%20Portfolio/task3/dashboard/)
2. Double-click the file [index.html](file:///f:/Data%20Analytics%20Internship%20Portfolio/task3/dashboard/index.html) to open the dashboard directly in any modern web browser. (No local server or installation required!).

### How to Host via GitHub Pages
To publish the dashboard to a live, public URL using GitHub Pages:
1. Go to the settings page of your GitHub repository: `https://github.com/dhanish0711/Data-Analytics-Portfolio/settings`.
2. Select **Pages** from the left-hand navigation sidebar.
3. Under **Build and deployment** > **Branch**, select the `main` branch and folder `/ (root)`, then click **Save**.
4. Within 1-2 minutes, GitHub will deploy your dashboard.
5. The live link will be:
   👉 **[Live Interactive Dashboard Link](https://dhanish0711.github.io/Data-Analytics-Portfolio/task3/dashboard/index.html)**

---
*Created as part of Task 3 for the Data Analytics Internship Portfolio.*
