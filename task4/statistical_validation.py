import os
import pandas as pd
import numpy as np
import scipy.stats as stats

# File paths
input_file = r"F:\Data Analytics Internship Portfolio\task1\cleaned_sales_dataset.xlsx"
output_dir = r"F:\Data Analytics Internship Portfolio\task4"
results_file = os.path.join(output_dir, "statistical_validation_results.txt")

def run_t_test(df):
    print("Running Welch's T-Test (Weekday vs Weekend spend)...")
    
    # Separate groups
    weekday_spend = df[~df['Is_Weekend']]['Total_Sales']
    weekend_spend = df[df['Is_Weekend']]['Total_Sales']
    
    # Summary stats
    n_wk = len(weekday_spend)
    n_we = len(weekend_spend)
    mean_wk = weekday_spend.mean()
    mean_we = weekend_spend.mean()
    std_wk = weekday_spend.std()
    std_we = weekend_spend.std()
    
    # Welch's t-test (equal_var=False)
    t_stat, p_val = stats.ttest_ind(weekday_spend, weekend_spend, equal_var=False)
    
    # Calculate 95% Confidence Interval for difference in means
    # Mean difference: Mean_weekday - Mean_weekend
    mean_diff = mean_wk - mean_we
    
    # Degrees of freedom for Welch's t-test (Satterthwaite approximation)
    s1_n1 = (std_wk**2) / n_wk
    s2_n2 = (std_we**2) / n_we
    df_welch = ((s1_n1 + s2_n2)**2) / ((s1_n1**2 / (n_wk - 1)) + (s2_n2**2 / (n_we - 1)))
    
    # Margin of error
    se_diff = np.sqrt(s1_n1 + s2_n2)
    t_crit = stats.t.ppf(0.975, df=df_welch)
    moe = t_crit * se_diff
    ci_lower = mean_diff - moe
    ci_upper = mean_diff + moe
    
    results = {
        "Test": "Two-Sample Independent Welch's T-Test",
        "Group_Weekday": {"n": n_wk, "mean": mean_wk, "std": std_wk},
        "Group_Weekend": {"n": n_we, "mean": mean_we, "std": std_we},
        "t_statistic": t_stat,
        "p_value": p_val,
        "degrees_of_freedom": df_welch,
        "mean_difference": mean_diff,
        "confidence_interval": (ci_lower, ci_upper)
    }
    return results

def run_chi_squared_test(df):
    print("Running Chi-Squared Test of Independence (Gender vs Category)...")
    
    # Create contingency table
    contingency_table = pd.crosstab(df['Gender'], df['Category'])
    
    # Run test
    chi2_stat, p_val, dof, expected = stats.chi2_contingency(contingency_table)
    
    results = {
        "Test": "Chi-Squared Test of Independence",
        "Contingency_Table": contingency_table,
        "Expected_Frequencies": pd.DataFrame(expected, index=contingency_table.index, columns=contingency_table.columns),
        "chi2_statistic": chi2_stat,
        "p_value": p_val,
        "degrees_of_freedom": dof
    }
    return results

def main():
    print("Starting Statistical Validation...")
    
    # Load dataset
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Cleaned dataset not found: {input_file}")
    df = pd.read_excel(input_file)
    
    # Run tests
    t_test_res = run_t_test(df)
    chi2_res = run_chi_squared_test(df)
    
    # Ensure output dir exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Write report
    with open(results_file, 'w', encoding='utf-8') as f:
        f.write("=== STATISTICAL VALIDATION & HYPOTHESIS TESTING RESULTS ===\n\n")
        
        # Welch's T-test
        f.write(f"### {t_test_res['Test']}\n")
        f.write("Hypothesis:\n")
        f.write("- Null Hypothesis (H0): Mean Weekday Spend = Mean Weekend Spend\n")
        f.write("- Alternative Hypothesis (H1): Mean Weekday Spend != Mean Weekend Spend\n\n")
        f.write("Summary Statistics:\n")
        f.write(f"- Weekdays: n = {t_test_res['Group_Weekday']['n']}, mean = ₹{t_test_res['Group_Weekday']['mean']:.2f}, std = ₹{t_test_res['Group_Weekday']['std']:.2f}\n")
        f.write(f"- Weekends: n = {t_test_res['Group_Weekend']['n']}, mean = ₹{t_test_res['Group_Weekend']['mean']:.2f}, std = ₹{t_test_res['Group_Weekend']['std']:.2f}\n\n")
        f.write("Test Results:\n")
        f.write(f"- t-statistic: {t_test_res['t_statistic']:.4f}\n")
        f.write(f"- p-value: {t_test_res['p_value']:.4f}\n")
        f.write(f"- Degrees of Freedom: {t_test_res['degrees_of_freedom']:.2f}\n")
        f.write(f"- Mean Difference: ₹{t_test_res['mean_difference']:.2f}\n")
        f.write(f"- 95% Confidence Interval of Difference: [₹{t_test_res['confidence_interval'][0]:.2f}, ₹{t_test_res['confidence_interval'][1]:.2f}]\n\n")
        
        significance = "STATISTICALLY SIGNIFICANT" if t_test_res['p_value'] < 0.05 else "NOT STATISTICALLY SIGNIFICANT"
        f.write(f"Conclusion: The difference in average transaction values between weekdays and weekends is {significance} (alpha = 0.05).\n")
        if t_test_res['p_value'] < 0.05:
            f.write("We reject the null hypothesis H0. There is evidence that weekday and weekend transactions differ in mean spend.\n")
        else:
            f.write("We fail to reject the null hypothesis H0. There is no statistical evidence that weekday and weekend transactions generate different mean spends.\n")
            
        f.write("\n" + "="*80 + "\n\n")
        
        # Chi-Squared Test
        f.write(f"### {chi2_res['Test']}\n")
        f.write("Hypothesis:\n")
        f.write("- Null Hypothesis (H0): Gender and Product Category choice are independent.\n")
        f.write("- Alternative Hypothesis (H1): Gender and Product Category choice are associated.\n\n")
        
        f.write("Observed Contingency Table:\n")
        f.write(chi2_res['Contingency_Table'].to_string())
        f.write("\n\nExpected Frequencies Table:\n")
        f.write(chi2_res['Expected_Frequencies'].round(2).to_string())
        f.write("\n\nTest Results:\n")
        f.write(f"- Chi-Squared statistic: {chi2_res['chi2_statistic']:.4f}\n")
        f.write(f"- p-value: {chi2_res['p_value']:.4f}\n")
        f.write(f"- Degrees of Freedom: {chi2_res['degrees_of_freedom']}\n\n")
        
        significance_chi = "STATISTICALLY SIGNIFICANT" if chi2_res['p_value'] < 0.05 else "NOT STATISTICALLY SIGNIFICANT"
        f.write(f"Conclusion: The association between customer gender and product category choice is {significance_chi} (alpha = 0.05).\n")
        if chi2_res['p_value'] < 0.05:
            f.write("We reject the null hypothesis H0. Gender and Product Category preferences are statistically associated.\n")
        else:
            f.write("We fail to reject the null hypothesis H0. Gender and Product Category are independent of each other.\n")
            
    print(f"Results successfully saved to: {results_file}")
    print("Statistical Validation completed successfully!")

if __name__ == "__main__":
    main()
