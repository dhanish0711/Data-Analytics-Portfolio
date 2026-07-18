# Task 4: Data Storytelling & Statistical Validation

## Objective
To synthesize all insights gathered from data wrangling, exploratory data analysis, and RFM customer segmentation into a compelling, business-focused narrative (the "Data Story") and mathematically validate key findings using statistical hypothesis testing.

---

## 1. The Data Story: Optimizing ApexPlanet Operations

### Executive Summary
Our analysis of 1,000 transactions reveals a healthy business generating **₹139.40 Million** in total sales with an Average Order Value (AOV) of **₹1,39,399.44**. The business operations are well-balanced geographically across tier-1 and tier-2 cities and balanced demographically between genders. However, key growth opportunities lie in **customer retention** (particularly reactivation of high-value dormant segments) and **operational efficiency** (marketing spend allocation).

### The Journey
1. **Ensuring Data Integrity (Part 1):** We began by cleansing the dataset, resolving sequential errors in `Order_ID` that grouped unrelated sales under a single ID, and imputing missing ages and cities. This step established a solid foundation of data reliability.
2. **Exploring the Drivers of Revenue (Part 2):** We discovered that **Electronics** (Laptops and Mobiles) is our primary revenue driver, contributing **36.4%** of sales share. Geographically, Patna, Kolkata, and Bengaluru generate the highest sales volume. Symmetrical gender distribution (51.1% Male, 48.9% Female) suggested a broad-market appeal rather than niche segment dominance.
3. **Understanding Customer Behavior (Part 3):** Deep-diving with RFM modeling revealed that **Loyal Customers** and **Champions** represent **39.6%** of our customer base, driving a major chunk of revenue. However, a significant retention risk was flagged: **15.2%** of customers are classified as **At Risk** (past high spenders who have gone dormant for over 200 days).
4. **Validating Hypotheses (Part 4):** To ensure these insights are statistically solid before recommending business adjustments, we performed statistical hypothesis testing.

---

## 2. Hypothesis Testing & Statistical Validation

We formulated and executed two statistical tests in Python using [statistical_validation.py](file:///f:/Data%20Analytics%20Internship%20Portfolio/task4/statistical_validation.py):

### Test 1: Weekday vs. Weekend Transaction Spend (Welch's T-Test)
* **Business Context:** The raw data showed that average order value (AOV) on weekdays (₹1,41,893) was slightly higher than on weekends (₹1,33,233). We wanted to determine if this difference is statistically significant to justify running weekend-specific pricing or promotional strategies.
* **Hypotheses:**
  - **Null Hypothesis ($H_0$):** There is no difference in the average transaction revenue between weekdays and weekends ($\mu_{\text{Weekday}} = \mu_{\text{Weekend}}$).
  - **Alternative Hypothesis ($H_1$):** There is a statistically significant difference in the average transaction revenue between weekdays and weekends ($\mu_{\text{Weekday}} \neq \mu_{\text{Weekend}}$).
* **Statistical Metrics:**
  - **t-statistic:** $1.0911$
  - **p-value:** $0.2757$
  - **95% Confidence Interval of Difference:** $[-₹6,931.24, ₹24,252.54]$
* **Business Conclusion:** Because the p-value ($0.2757$) is much greater than our significance level ($\alpha = 0.05$), **we fail to reject the null hypothesis**. The ₹8,660 difference in mean spend is statistically insignificant and likely due to random sampling variation. 
* **Action:** Marketing ad-spend and pricing structures should be deployed **uniformly** across the week. There is no mathematical justification for paying a premium for weekend ad placement.

---

### Test 2: Gender vs. Product Category Preferences (Chi-Squared Test of Independence)
* **Business Context:** We wanted to determine if customer gender influences their choice of product categories, which directly impacts catalog recommendations and gender-specific ad targeting.
* **Hypotheses:**
  - **Null Hypothesis ($H_0$):** Customer gender and product category choice are independent.
  - **Alternative Hypothesis ($H_1$):** Customer gender and product category choice are associated (dependent).
* **Observed vs. Expected Highlights:**
  - Symmetrical baseline expected frequencies: e.g. Electronics was expected to attract 173.11 females and 180.89 males.
  - Actual values showed minor deviations: Females bought slightly more Fashion (89 observed vs 76.28 expected); Males bought slightly more Electronics (196 observed vs 180.89 expected).
* **Statistical Metrics:**
  - **Chi-Squared Statistic:** $9.0936$
  - **p-value:** $0.0588$
  - **Degrees of Freedom:** 4
* **Business Conclusion:** The p-value ($0.0588$) is slightly higher than $\alpha = 0.05$. Therefore, **we fail to reject the null hypothesis** at the 95% confidence level. Customer gender and product category choice are statistically independent.
* **Action:** While a weak marginal trend is visible (slight male skew in electronics and female skew in fashion), high-budget marketing campaigns should **not** strictly divide budgets or inventory placements based on gender. A unified, gender-neutral marketing strategy is recommended for high-performing categories like Electronics and Furniture.

*The full statistical execution details are recorded in: [statistical_validation_results.txt](file:///f:/Data%20Analytics%20Internship%20Portfolio/task4/statistical_validation_results.txt).*

---

## 3. Reveal.js Slide Deck Presentation

We designed an interactive presentation deck inside [task4/presentation/](file:///f:/Data%20Analytics%20Internship%20Portfolio/task4/presentation/) to share these results with stakeholders.

### How to View the Slide Deck
* **Locally:** Double-click the file [index.html](file:///f:/Data%20Analytics%20Internship%20Portfolio/task4/presentation/index.html) to open the slides directly in your browser. Use your keyboard arrow keys or spacebar to navigate.
* **Live Link (GitHub Pages):**
  👉 **[Live Reveal.js Presentation Link](https://dhanish0711.github.io/Data-Analytics-Portfolio/task4/presentation/index.html)**

---
*Created as part of Task 4 for the Data Analytics Internship Portfolio.*
