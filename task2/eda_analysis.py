import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# File paths
input_file = r"F:\Data Analytics Internship Portfolio\task1\cleaned_sales_dataset.xlsx"
output_dir = r"F:\Data Analytics Internship Portfolio\task2"
images_dir = os.path.join(output_dir, "images")
stats_file = os.path.join(output_dir, "descriptive_statistics.txt")

def setup_directories():
    os.makedirs(images_dir, exist_ok=True)
    print(f"Directory verified: {images_dir}")

def generate_descriptive_stats(df):
    print("Generating descriptive statistics...")
    
    # Numerical description
    num_summary = df[['Age', 'Quantity', 'Unit_Price', 'Total_Sales']].describe()
    
    # Categorical counts and descriptions
    cat_cols = ['Gender', 'City', 'Product', 'Category', 'Age_Group', 'Order_DayOfWeek']
    cat_summaries = []
    for col in cat_cols:
        counts = df[col].value_counts()
        pct = df[col].value_counts(normalize=True) * 100
        summary_df = pd.DataFrame({'Count': counts, 'Percentage': pct})
        cat_summaries.append(f"\n--- Categorical Summary: {col} ---\n{summary_df.to_string()}")

    # Write summary statistics to text file
    with open(stats_file, 'w', encoding='utf-8') as f:
        f.write("=== DESCRIPTIVE STATISTICS & UNIVARIATE ANALYSIS ===\n\n")
        f.write("--- Numerical Variables Summary ---\n")
        f.write(num_summary.to_string())
        f.write("\n\n")
        f.write("--- Categorical Variables Summaries ---")
        for summary in cat_summaries:
            f.write(summary)
            f.write("\n")
            
    print(f"Saved descriptive statistics to: {stats_file}")

def plot_age_distribution(df):
    print("Generating Age distribution plot...")
    plt.figure(figsize=(8, 5))
    
    # Define custom colors and style
    # Use a modern styling: clean slate blue bars with a subtle black border
    counts, bins, patches = plt.hist(df['Age'], bins=15, color='#4A90E2', edgecolor='#212529', alpha=0.85, density=False)
    
    # Styling details
    plt.title("Distribution of Customer Age", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Age", fontsize=12, labelpad=10)
    plt.ylabel("Number of Customers", fontsize=12, labelpad=10)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.gca().set_axisbelow(True) # Ensure gridlines are behind bars
    
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "age_distribution.png"), dpi=150)
    plt.close()

def plot_sales_by_category(df):
    print("Generating Sales by Category plot...")
    plt.figure(figsize=(9, 5))
    
    # Aggregate sales by category
    sales_by_cat = df.groupby('Category')['Total_Sales'].sum().sort_values(ascending=True)
    
    # Modern horizontal bar chart with curated colors
    colors = ['#B8E986', '#F5A623', '#F8E71C', '#9B51E0', '#4A90E2'] # Curated colors
    bars = plt.barh(sales_by_cat.index, sales_by_cat.values, color=colors[:len(sales_by_cat)], edgecolor='#212529')
    
    # Add text labels on the bars showing sales in thousands
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 10000, bar.get_y() + bar.get_height()/2, f"₹{width/1e6:.2f}M",
                 va='center', ha='left', fontsize=10, fontweight='bold')
                 
    plt.title("Total Sales Revenue by Product Category", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Total Sales (INR)", fontsize=12, labelpad=10)
    plt.ylabel("Category", fontsize=12, labelpad=10)
    
    # Format x-axis labels as currency in Millions
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"₹{x/1e6:.1f}M"))
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    plt.gca().set_axisbelow(True)
    
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "sales_by_category.png"), dpi=150)
    plt.close()

def plot_orders_by_city(df):
    print("Generating Orders by City plot...")
    plt.figure(figsize=(9, 5))
    
    # Count orders by city and sort
    orders_by_city = df['City'].value_counts().sort_values(ascending=False)
    
    # Modern vertical bar chart
    plt.bar(orders_by_city.index, orders_by_city.values, color='#50E3C2', edgecolor='#212529', width=0.6)
    
    # Annotate bar values
    for i, val in enumerate(orders_by_city.values):
        plt.text(i, val + 2, str(val), ha='center', va='bottom', fontsize=9, fontweight='bold')
        
    plt.title("Order Volume by City", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("City", fontsize=12, labelpad=10)
    plt.ylabel("Number of Orders", fontsize=12, labelpad=10)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.gca().set_axisbelow(True)
    plt.xticks(rotation=15)
    
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "orders_by_city.png"), dpi=150)
    plt.close()

def plot_gender_distribution(df):
    print("Generating Gender distribution plot...")
    plt.figure(figsize=(6, 6))
    
    gender_counts = df['Gender'].value_counts()
    
    # Custom colors: Coral and Navy Blue
    colors = ['#FF6B6B', '#1A5F7A']
    
    # Create donut chart
    plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=90,
            colors=colors, wedgeprops={'edgecolor': 'white', 'linewidth': 2, 'antialiased': True},
            textprops={'fontsize': 11, 'fontweight': 'bold'}, pctdistance=0.7)
            
    # Add a circle in the center to make it a donut chart
    centre_circle = plt.Circle((0,0), 0.50, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    
    plt.title("Transaction Volume Share by Gender", fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "gender_distribution.png"), dpi=150)
    plt.close()

def plot_correlation_heatmap(df):
    print("Generating Correlation Heatmap plot...")
    # Select numerical columns
    num_cols = ['Age', 'Quantity', 'Unit_Price', 'Total_Sales']
    corr_matrix = df[num_cols].corr()
    
    fig, ax = plt.subplots(figsize=(7, 6))
    
    # Plot matrix using imshow with coolwarm colormap
    cax = ax.imshow(corr_matrix.values, cmap='coolwarm', vmin=-1, vmax=1)
    
    # Add colorbar
    fig.colorbar(cax, fraction=0.046, pad=0.04)
    
    # Set labels
    ax.set_xticks(np.arange(len(num_cols)))
    ax.set_yticks(np.arange(len(num_cols)))
    ax.set_xticklabels(num_cols, fontsize=10, fontweight='bold')
    ax.set_yticklabels(num_cols, fontsize=10, fontweight='bold')
    
    # Add correlation coefficients inside the cells
    for i in range(len(num_cols)):
        for j in range(len(num_cols)):
            val = corr_matrix.iloc[i, j]
            color = 'black' if abs(val) < 0.6 else 'white'
            ax.text(j, i, f"{val:.3f}", ha='center', va='center', color=color, fontsize=11, fontweight='bold')
            
    plt.title("Correlation Matrix of Numeric Features", fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "correlation_heatmap.png"), dpi=150)
    plt.close()

def plot_sales_boxplot(df):
    print("Generating Sales by Category boxplot...")
    plt.figure(figsize=(9, 6))
    
    categories = df['Category'].unique()
    data_by_cat = [df[df['Category'] == cat]['Total_Sales'].values for cat in categories]
    
    # Custom colored boxes
    box = plt.boxplot(data_by_cat, tick_labels=categories, patch_artist=True,
                      boxprops=dict(facecolor='#DDA0DD', edgecolor='#212529'),
                      medianprops=dict(color='red', linewidth=1.5),
                      flierprops=dict(marker='o', markerfacecolor='#FF6B6B', markersize=4, alpha=0.5))
                      
    # Color each box differently
    colors = ['#FFD166', '#EF476F', '#06D6A0', '#118AB2', '#073B4C']
    for patch, color in zip(box['boxes'], colors[:len(categories)]):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
        
    plt.title("Distribution of Transaction Sales Value by Category", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Category", fontsize=12, labelpad=10)
    plt.ylabel("Total Sales (INR)", fontsize=12, labelpad=10)
    
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"₹{x/1e3:.0f}K"))
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.gca().set_axisbelow(True)
    
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "sales_by_category_boxplot.png"), dpi=150)
    plt.close()

def plot_age_by_category_stacked(df):
    print("Generating Age Group vs Category stacked bar plot...")
    # Generate cross-tabulation
    ct = pd.crosstab(df['Category'], df['Age_Group'])
    
    # Normalize by row to show percentages
    ct_pct = ct.div(ct.sum(axis=1), axis=0) * 100
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot stacked bar chart
    colors = ['#264653', '#2A9D8F', '#E76F51']
    ct_pct.plot(kind='bar', stacked=True, color=colors, ax=ax, edgecolor='#212529', width=0.55)
    
    # Add text labels inside bars
    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f%%', label_type='center', fontsize=9, fontweight='bold', color='white')
        
    plt.title("Customer Age Demographic Share by Product Category", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Category", fontsize=12, labelpad=10)
    plt.ylabel("Demographic Percentage (%)", fontsize=12, labelpad=10)
    
    plt.legend(title="Age Demographic", bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.4)
    plt.gca().set_axisbelow(True)
    
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "age_by_category_stacked.png"), dpi=150)
    plt.close()

def main():
    print("Starting EDA Analysis...")
    setup_directories()
    
    # Load dataset
    df = pd.read_excel(input_file)
    
    # Generate statistics
    generate_descriptive_stats(df)
    
    # Generate plots
    plot_age_distribution(df)
    plot_sales_by_category(df)
    plot_orders_by_city(df)
    plot_gender_distribution(df)
    plot_correlation_heatmap(df)
    plot_sales_boxplot(df)
    plot_age_by_category_stacked(df)
    
    print("All EDA Analysis plots and descriptive statistics generated successfully!")

if __name__ == "__main__":
    main()
