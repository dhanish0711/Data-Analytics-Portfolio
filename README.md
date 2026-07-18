# Data Analytics Internship Portfolio - Master Repository

Welcome to the master repository for my **Data Analytics Internship Portfolio**. This repository serves as a unified, polished, single point of reference containing all code, analytical models, interactive dashboards, slide presentations, and statistical validations completed during my internship.

---

## 1. Master Portfolio Landing Page (Live)

We have built a premium, browser-native personal portfolio landing page website at [index.html](file:///f:/Data%20Analytics%20Internship%20Portfolio/index.html) in the repository root. This landing page acts as a visual showcase of the entire internship and provides quick access buttons to launch the interactive deliverables.

### How to Access the Live Portfolio
- **Locally:** Double-click the file [index.html](file:///f:/Data%20Analytics%20Internship%20Portfolio/index.html) to open the landing page directly in your browser.
- **Live Link (GitHub Pages):**
  👉 **[Live Portfolio Website Link](https://dhanish0711.github.io/Data-Analytics-Portfolio/index.html)**
  *(Note: To activate this link, follow the simple deployment instructions in Section 5 below).*

---

## 2. Repository Structure & Project Modules

All tasks are organized systematically into task-specific folders:

### 📂 [task1/](file:///f:/Data%20Analytics%20Internship%20Portfolio/task1/) - Data Immersion & Wrangling
* **Focus:** Data profiling, quality audits, sequence reconstruction, and imputation.
* **Key Code:** [data_cleaning.py](file:///f:/Data%20Analytics%20Internship%20Portfolio/task1/data_cleaning.py) (Reproducible Pandas pipeline).
* **Deliverables:** Cleaned transaction data in Excel ([cleaned_sales_dataset.xlsx](file:///f:/Data%20Analytics%20Internship%20Portfolio/task1/cleaned_sales_dataset.xlsx)) and CSV ([cleaned_sales_dataset.csv](file:///f:/Data%20Analytics%20Internship%20Portfolio/task1/cleaned_sales_dataset.csv)).
* **Documentation:** [task1/README.md](file:///f:/Data%20Analytics%20Internship%20Portfolio/task1/README.md) (Complete Data Dictionary and Data Quality Assessment report).

### 📂 [task2/](file:///f:/Data%20Analytics%20Internship%20Portfolio/task2/) - Exploratory Data Analysis (EDA) & SQL BI
* **Focus:** Summary statistics, data distributions, correlation profiling, and SQL query scripting.
* **Key Code:**
  - [eda_analysis.py](file:///f:/Data%20Analytics%20Internship%20Portfolio/task2/eda_analysis.py) (Visualizations generator).
  - [sql_queries.py](file:///f:/Data%20Analytics%20Internship%20Portfolio/task2/sql_queries.py) (SQLite DB populator and query runner).
* **Deliverables:** Relational SQLite DB ([task2_database.db](file:///f:/Data%20Analytics%20Internship%20Portfolio/task2/task2_database.db)) containing normalized tables (`sales`, `products`, `regions`), 7 generated charts in `task2/images/`, and a query log ([sql_queries_output.txt](file:///f:/Data%20Analytics%20Internship%20Portfolio/task2/sql_queries_output.txt)).
* **Documentation:** [task2/README.md](file:///f:/Data%20Analytics%20Internship%20Portfolio/task2/README.md) (Detailed EDA profiling, box plots, stacked demographic charts, and SQL results).

### 📂 [task3/](file:///f:/Data%20Analytics%20Internship%20Portfolio/task3/) - Deep-Dive Analysis & Interactive Dashboarding
* **Focus:** Behavioral customer segmentation (RFM) and interactive web application dashboarding.
* **Key Code:**
  - [customer_segmentation.py](file:///f:/Data%20Analytics%20Internship%20Portfolio/task3/customer_segmentation.py) (RFM model scoring script).
  - [dashboard/app.js](file:///f:/Data%20Analytics%20Internship%20Portfolio/task3/dashboard/app.js) (Dashboard controller script).
* **Deliverables:** RFM profile data ([segmented_customers.csv](file:///f:/Data%20Analytics%20Internship%20Portfolio/task3/segmented_customers.csv)), and a glassmorphic dashboard interface ([dashboard/index.html](file:///f:/Data%20Analytics%20Internship%20Portfolio/task3/dashboard/index.html)) connecting to JSON transaction data.
* **Live Link:** 👉 **[Live Interactive Dashboard Link](https://dhanish0711.github.io/Data-Analytics-Portfolio/task3/dashboard/index.html)**
* **Documentation:** [task3/README.md](file:///f:/Data%20Analytics%20Internship%20Portfolio/task3/README.md) (RFM cohort classifications, customer counts, and strategic action plans).

### 📂 [task4/](file:///f:/Data%20Analytics%20Internship%20Portfolio/task4/) - Data Storytelling & Statistical Validation
* **Focus:** Welch's T-Test and Chi-Squared hypothesis testing, and custom visual presentation design.
* **Key Code:** [statistical_validation.py](file:///f:/Data%20Analytics%20Internship%20Portfolio/task4/statistical_validation.py) (Scipy statistical testing script).
* **Deliverables:** Statistical results log ([statistical_validation_results.txt](file:///f:/Data%20Analytics%20Internship%20Portfolio/task4/statistical_validation_results.txt)), and a custom, large 10-slide glassmorphic presentation deck ([presentation/index.html](file:///f:/Data%20Analytics%20Internship%20Portfolio/task4/presentation/index.html)).
* **Live Link:** 👉 **[Live Reveal.js Presentation Link](https://dhanish0711.github.io/Data-Analytics-Portfolio/task4/presentation/index.html)**
* **Documentation:** [task4/README.md](file:///f:/Data%20Analytics%20Internship%20Portfolio/task4/README.md) (Cohesive Data Story, hypothesis math definitions, p-values, and business decisions).

---

## 3. Technical Stack & Competencies

* **Programming:** Python 3 (Pandas, SciPy, Matplotlib, NumPy, OpenPyXL).
* **Databases:** Relational database schemas, normalized table designs, constraints, and standard SQL queries (sqlite3).
* **Statistics:** Hypothesis testing, probability distributions, Welch's t-test, Chi-squared contingency tables, p-value evaluations, and confidence intervals.
* **Business Intelligence (BI):** RFM (Recency, Frequency, Monetary) modeling, behavioral customer profiling, interactive dashboard layouts (Tailwind CSS, Vanilla HTML/JS, Chart.js), and dashboard mockup design.
* **Version Control & Deployment:** Git, remote GitHub repository tracking, and automated hosting via GitHub Pages.

---

## 4. Key Learnings & Reflection

1. **Ensuring Data Integrity:** Raw datasets contain corruptions (like the sequence `Order_ID` duplicates found here) that must be programmatically audited and cleaned using reproducible code before any business intelligence can be extracted.
2. **Behavioral Target Alignment:** Customer segmentation models like RFM are vital for marketing operations. Grouping buyers into actionable cohorts (Champions, Loyal, At Risk) helps optimize retention spend by identifying exactly who is dormant but high-value.
3. **Statistical Validation over Intuition:** High variances can render raw numeric averages misleading. Hypothesis tests (Welch's t-test and Chi-squared) mathematically prove if differences are real or random noise, preventing companies from wasting resources on false weekday/weekend premiums.

---

## 5. GitHub Pages Deployment Guide

To deploy this entire visual portfolio (the landing page, the live dashboard, and the slide deck) to a public URL:
1. Open your repository settings page: `https://github.com/dhanish0711/Data-Analytics-Portfolio/settings`.
2. Click on **Pages** in the left-hand navigation menu.
3. Under **Build and deployment** > **Branch**, select `main` from the dropdown and leave the folder set to `/ (root)`.
4. Click **Save**.
5. Within 1-2 minutes, GitHub will deploy your pages. The live links will be:
   - **Main Portfolio Website:** `https://dhanish0711.github.io/Data-Analytics-Portfolio/index.html`
   - **Interactive BI Dashboard:** `https://dhanish0711.github.io/Data-Analytics-Portfolio/task3/dashboard/index.html`
   - **Visual Presentation Slides:** `https://dhanish0711.github.io/Data-Analytics-Portfolio/task4/presentation/index.html`

---
*Internship Capstone Portfolio. Dhanish Ladwani - Data Analytics.*
