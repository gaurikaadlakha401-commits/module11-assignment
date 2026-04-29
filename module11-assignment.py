# Module 11 Assignment: Data Visualization with Matplotlib
# SunCoast Retail Visual Analysis

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Welcome message
print("=" * 60)
print("SUNCOAST RETAIL VISUAL ANALYSIS")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO CREATE SAMPLE DATA (DO NOT MODIFY) -----
# Create a seed for reproducibility
np.random.seed(42)

# Generate dates for 8 quarters (Q1 2022 - Q4 2023)
quarters = pd.date_range(start='2022-01-01', periods=8, freq='Q')
quarter_labels = ['Q1 2022', 'Q2 2022', 'Q3 2022', 'Q4 2022',
                 'Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023']

# Store locations
locations = ['Tampa', 'Miami', 'Orlando', 'Jacksonville']

# Product categories
categories = ['Electronics', 'Clothing', 'Home Goods', 'Sporting Goods', 'Beauty']

# Generate quarterly sales data for each location and category
quarterly_data = []

for quarter_idx, quarter in enumerate(quarters):
    for location in locations:
        for category in categories:
            # Base sales with seasonal pattern (Q4 higher, Q1 lower)
            base_sales = np.random.normal(loc=100000, scale=20000)
            seasonal_factor = 1.0
            if quarter.quarter == 4:  # Q4 (holiday boost)
                seasonal_factor = 1.3
            elif quarter.quarter == 1:  # Q1 (post-holiday dip)
                seasonal_factor = 0.8

            # Location effect
            location_factor = {
                'Tampa': 1.0,
                'Miami': 1.2,
                'Orlando': 0.9,
                'Jacksonville': 0.8
            }[location]

            # Category effect
            category_factor = {
                'Electronics': 1.5,
                'Clothing': 1.0,
                'Home Goods': 0.8,
                'Sporting Goods': 0.7,
                'Beauty': 0.9
            }[category]

            # Growth trend over time (5% per year, quarterly compounded)
            growth_factor = (1 + 0.05/4) ** quarter_idx

            # Calculate sales with some randomness
            sales = base_sales * seasonal_factor * location_factor * category_factor * growth_factor
            sales = sales * np.random.normal(loc=1.0, scale=0.1)  # Add noise

            # Advertising spend (correlated with sales but with diminishing returns)
            ad_spend = (sales ** 0.7) * 0.05 * np.random.normal(loc=1.0, scale=0.2)

            # Record
            quarterly_data.append({
                'Quarter': quarter,
                'QuarterLabel': quarter_labels[quarter_idx],
                'Location': location,
                'Category': category,
                'Sales': round(sales, 2),
                'AdSpend': round(ad_spend, 2),
                'Year': quarter.year
            })

# Create customer data
customer_data = []
total_customers = 2000

# Age distribution parameters for each location
age_params = {
    'Tampa': (45, 15),      # Older demographic
    'Miami': (35, 12),      # Younger demographic
    'Orlando': (38, 14),    # Mixed demographic
    'Jacksonville': (42, 13)  # Middle-aged demographic
}

for location in locations:
    # Generate ages based on location demographics
    mean_age, std_age = age_params[location]
    customer_count = int(total_customers * {
        'Tampa': 0.3,
        'Miami': 0.35,
        'Orlando': 0.2,
        'Jacksonville': 0.15
    }[location])

    ages = np.random.normal(loc=mean_age, scale=std_age, size=customer_count)
    ages = np.clip(ages, 18, 80).astype(int)  # Ensure ages are between 18-80

    # Generate purchase amounts
    for age in ages:
        # Younger and older customers spend differently across categories
        if age < 30:
            category_preference = np.random.choice(categories, p=[0.3, 0.3, 0.1, 0.2, 0.1])
        elif age < 50:
            category_preference = np.random.choice(categories, p=[0.25, 0.2, 0.25, 0.15, 0.15])
        else:
            category_preference = np.random.choice(categories, p=[0.15, 0.1, 0.35, 0.1, 0.3])

        # Purchase amount based on age and category
        base_amount = np.random.gamma(shape=5, scale=20)

        # Product tier (budget, mid-range, premium)
        price_tier = np.random.choice(['Budget', 'Mid-range', 'Premium'],
                                     p=[0.3, 0.5, 0.2])

        tier_factor = {'Budget': 0.7, 'Mid-range': 1.0, 'Premium': 1.8}[price_tier]

        purchase_amount = base_amount * tier_factor

        customer_data.append({
            'Location': location,
            'Age': age,
            'Category': category_preference,
            'PurchaseAmount': round(purchase_amount, 2),
            'PriceTier': price_tier
        })

# Create DataFrames
sales_df = pd.DataFrame(quarterly_data)
customer_df = pd.DataFrame(customer_data)

# Add some calculated columns
sales_df['Quarter_Num'] = sales_df['Quarter'].dt.quarter
sales_df['SalesPerDollarSpent'] = sales_df['Sales'] / sales_df['AdSpend']

# Print data info
print("\nSales Data Sample:")
print(sales_df.head())
print("\nCustomer Data Sample:")
print(customer_df.head())
print("\nDataFrames created successfully. Ready for visualization!")
# ----- END OF DATA CREATION -----


# TODO 1: Time Series Visualization - Sales Trends
def plot_quarterly_sales_trend():
    """
    Create a line chart showing total sales for each quarter.
    REQUIRED: Return the figure object
    """
    quarterly_sales = sales_df.groupby('QuarterLabel')['Sales'].sum().reindex(quarter_labels)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(quarterly_sales.index, quarterly_sales.values, marker='o', linewidth=2)
    ax.set_title('Overall Quarterly Sales Trend')
    ax.set_xlabel('Quarter')
    ax.set_ylabel('Total Sales ($)')
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


def plot_location_sales_comparison():
    """
    Create a multi-line chart comparing quarterly sales across different locations.
    REQUIRED: Return the figure object
    """
    location_sales = sales_df.groupby(['QuarterLabel', 'Location'])['Sales'].sum().unstack()
    location_sales = location_sales.reindex(quarter_labels)

    fig, ax = plt.subplots(figsize=(10, 5))
    markers = ['o', 's', '^', 'D']

    for i, location in enumerate(location_sales.columns):
        ax.plot(location_sales.index, location_sales[location], marker=markers[i], linewidth=2, label=location)

    ax.set_title('Quarterly Sales Trends by Location')
    ax.set_xlabel('Quarter')
    ax.set_ylabel('Total Sales ($)')
    ax.legend(title='Location')
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


# TODO 2: Categorical Comparison - Product Performance by Location
def plot_category_performance_by_location():
    """
    Create a grouped bar chart showing how each product category performs in different locations.
    REQUIRED: Return the figure object
    """
    latest_quarter = sales_df['Quarter'].max()
    latest_data = sales_df[sales_df['Quarter'] == latest_quarter]
    grouped = latest_data.groupby(['Category', 'Location'])['Sales'].sum().unstack()

    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(categories))
    width = 0.2

    for i, location in enumerate(locations):
        ax.bar(x + i * width, grouped[location].reindex(categories), width=width, label=location)

    ax.set_title('Category Performance by Location (Most Recent Quarter)')
    ax.set_xlabel('Product Category')
    ax.set_ylabel('Sales ($)')
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(categories, rotation=20)
    ax.legend(title='Location')
    plt.tight_layout()
    return fig


def plot_sales_composition_by_location():
    """
    Create a stacked bar chart showing the composition of sales across categories for each location.
    REQUIRED: Return the figure object
    """
    sales_by_loc_cat = sales_df.groupby(['Location', 'Category'])['Sales'].sum().unstack()
    sales_pct = sales_by_loc_cat.div(sales_by_loc_cat.sum(axis=1), axis=0) * 100

    fig, ax = plt.subplots(figsize=(10, 6))
    bottom = np.zeros(len(sales_pct))

    for category in categories:
        values = sales_pct[category].reindex(locations)
        ax.bar(locations, values, bottom=bottom, label=category)
        bottom += values.values

    ax.set_title('Sales Composition by Location')
    ax.set_xlabel('Location')
    ax.set_ylabel('Percentage of Total Sales (%)')
    ax.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    return fig


# TODO 3: Relationship Analysis - Advertising and Sales
def plot_ad_spend_vs_sales():
    """
    Create a scatter plot to visualize the relationship between advertising spend and sales.
    REQUIRED: Return the figure object
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(sales_df['AdSpend'], sales_df['Sales'], alpha=0.7)

    m, b = np.polyfit(sales_df['AdSpend'], sales_df['Sales'], 1)
    x_vals = np.linspace(sales_df['AdSpend'].min(), sales_df['AdSpend'].max(), 100)
    ax.plot(x_vals, m * x_vals + b, linestyle='--', label='Best-Fit Line')

    # annotate top 3 sales outliers
    outliers = sales_df.nlargest(3, 'Sales')
    for _, row in outliers.iterrows():
        ax.annotate(f"{row['Location']} - {row['Category']}",
                    (row['AdSpend'], row['Sales']),
                    textcoords="offset points",
                    xytext=(5, 5),
                    fontsize=8)

    ax.set_title('Advertising Spend vs Sales')
    ax.set_xlabel('Advertising Spend ($)')
    ax.set_ylabel('Sales ($)')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    return fig


def plot_ad_efficiency_over_time():
    """
    Create a line chart showing how efficient advertising spend has been over time.
    REQUIRED: Return the figure object
    """
    ad_efficiency = sales_df.groupby('QuarterLabel')['SalesPerDollarSpent'].mean().reindex(quarter_labels)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(ad_efficiency.index, ad_efficiency.values, marker='o', linewidth=2)
    ax.set_title('Advertising Efficiency Over Time')
    ax.set_xlabel('Quarter')
    ax.set_ylabel('Average Sales Per Advertising Dollar')
    ax.grid(True, linestyle='--', alpha=0.6)

    max_q = ad_efficiency.idxmax()
    max_val = ad_efficiency.max()
    ax.annotate(f'Peak: {max_q}', xy=(max_q, max_val), xytext=(0, 10),
                textcoords='offset points', ha='center')

    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


# TODO 4: Distribution Analysis - Customer Demographics
def plot_customer_age_distribution():
    """
    Create histograms showing the age distribution of customers, both overall and by location.
    REQUIRED: Return the figure object
    """
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    axes = axes.flatten()

    # Overall
    axes[0].hist(customer_df['Age'], bins=15, edgecolor='black')
    axes[0].axvline(customer_df['Age'].mean(), linestyle='--', label='Mean')
    axes[0].axvline(customer_df['Age'].median(), linestyle=':', label='Median')
    axes[0].set_title('Overall Age Distribution')
    axes[0].set_xlabel('Age')
    axes[0].set_ylabel('Frequency')
    axes[0].legend()

    # By location
    for i, location in enumerate(locations, start=1):
        loc_ages = customer_df[customer_df['Location'] == location]['Age']
        axes[i].hist(loc_ages, bins=15, edgecolor='black')
        axes[i].axvline(loc_ages.mean(), linestyle='--', label='Mean')
        axes[i].axvline(loc_ages.median(), linestyle=':', label='Median')
        axes[i].set_title(f'{location} Age Distribution')
        axes[i].set_xlabel('Age')
        axes[i].set_ylabel('Frequency')
        axes[i].legend()

    # Hide extra subplot
    axes[5].axis('off')

    plt.tight_layout()
    return fig


def plot_purchase_by_age_group():
    """
    Create box plots showing purchase amounts across different age groups.
    REQUIRED: Return the figure object
    """
    customer_df['AgeGroup'] = pd.cut(
        customer_df['Age'],
        bins=[18, 30, 45, 60, 80],
        labels=['18-30', '31-45', '46-60', '61+'],
        include_lowest=True
    )

    data = [customer_df[customer_df['AgeGroup'] == group]['PurchaseAmount'] for group in ['18-30', '31-45', '46-60', '61+']]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.boxplot(data, labels=['18-30', '31-45', '46-60', '61+'])
    ax.set_title('Purchase Amount by Age Group')
    ax.set_xlabel('Age Group')
    ax.set_ylabel('Purchase Amount ($)')
    plt.tight_layout()
    return fig


# TODO 5: Sales Distribution - Pricing Tiers
def plot_purchase_amount_distribution():
    """
    Create a histogram showing the distribution of purchase amounts.
    REQUIRED: Return the figure object
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(customer_df['PurchaseAmount'], bins=20, edgecolor='black')
    ax.set_title('Distribution of Purchase Amounts')
    ax.set_xlabel('Purchase Amount ($)')
    ax.set_ylabel('Frequency')
    plt.tight_layout()
    return fig


def plot_sales_by_price_tier():
    """
    Create a pie chart showing the breakdown of sales by price tier.
    REQUIRED: Return the figure object
    """
    price_tier_sales = customer_df.groupby('PriceTier')['PurchaseAmount'].sum().reindex(['Budget', 'Mid-range', 'Premium'])
    explode = [0, 0, 0]
    largest_idx = price_tier_sales.values.argmax()
    explode[largest_idx] = 0.1

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(price_tier_sales.values,
           labels=price_tier_sales.index,
           autopct='%1.1f%%',
           explode=explode,
           startangle=90)
    ax.set_title('Sales Breakdown by Price Tier')
    plt.tight_layout()
    return fig


# TODO 6: Market Share Analysis
def plot_category_market_share():
    """
    Create a pie chart showing the market share of each product category.
    REQUIRED: Return the figure object
    """
    category_sales = sales_df.groupby('Category')['Sales'].sum().reindex(categories)
    explode = [0] * len(category_sales)
    explode[category_sales.values.argmax()] = 0.1

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(category_sales.values,
           labels=category_sales.index,
           autopct='%1.1f%%',
           explode=explode,
           startangle=90)
    ax.set_title('Market Share by Product Category')
    plt.tight_layout()
    return fig


def plot_location_sales_distribution():
    """
    Create a pie chart showing the distribution of sales across different store locations.
    REQUIRED: Return the figure object
    """
    location_sales = sales_df.groupby('Location')['Sales'].sum().reindex(locations)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(location_sales.values,
           labels=location_sales.index,
           autopct='%1.1f%%',
           startangle=90)
    ax.set_title('Sales Distribution by Location')
    plt.tight_layout()
    return fig


# TODO 7: Comprehensive Dashboard
def create_business_dashboard():
    """
    Create a comprehensive dashboard with multiple subplots highlighting key business insights.
    REQUIRED: Return the figure object with at least 4 subplots
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('SunCoast Retail Business Dashboard', fontsize=16)

    # 1. Quarterly sales trend
    quarterly_sales = sales_df.groupby('QuarterLabel')['Sales'].sum().reindex(quarter_labels)
    axes[0, 0].plot(quarterly_sales.index, quarterly_sales.values, marker='o')
    axes[0, 0].set_title('Quarterly Sales Trend')
    axes[0, 0].tick_params(axis='x', rotation=45)

    # 2. Sales by location
    location_sales = sales_df.groupby('Location')['Sales'].sum().reindex(locations)
    axes[0, 1].bar(location_sales.index, location_sales.values)
    axes[0, 1].set_title('Total Sales by Location')
    axes[0, 1].tick_params(axis='x', rotation=20)

    # 3. Ad spend vs sales
    axes[1, 0].scatter(sales_df['AdSpend'], sales_df['Sales'], alpha=0.7)
    axes[1, 0].set_title('Ad Spend vs Sales')
    axes[1, 0].set_xlabel('Ad Spend')
    axes[1, 0].set_ylabel('Sales')

    # 4. Price tier sales
    price_tier_sales = customer_df.groupby('PriceTier')['PurchaseAmount'].sum().reindex(['Budget', 'Mid-range', 'Premium'])
    axes[1, 1].pie(price_tier_sales.values, labels=price_tier_sales.index, autopct='%1.1f%%', startangle=90)
    axes[1, 1].set_title('Sales by Price Tier')

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    return fig


# Main function to execute all visualizations
def main():
    print("\n" + "=" * 60)
    print("SUNCOAST RETAIL VISUAL ANALYSIS RESULTS")
    print("=" * 60)

    # Time Series Analysis
    fig1 = plot_quarterly_sales_trend()
    fig2 = plot_location_sales_comparison()

    # Categorical Comparison
    fig3 = plot_category_performance_by_location()
    fig4 = plot_sales_composition_by_location()

    # Relationship Analysis
    fig5 = plot_ad_spend_vs_sales()
    fig6 = plot_ad_efficiency_over_time()

    # Distribution Analysis
    fig7 = plot_customer_age_distribution()
    fig8 = plot_purchase_by_age_group()

    # Sales Distribution
    fig9 = plot_purchase_amount_distribution()
    fig10 = plot_sales_by_price_tier()

    # Market Share Analysis
    fig11 = plot_category_market_share()
    fig12 = plot_location_sales_distribution()

    # Comprehensive Dashboard
    fig13 = create_business_dashboard()

    # Business insights summary
    print("\nKEY BUSINESS INSIGHTS:")
    print("1. Sales generally trend upward over time, with noticeable Q4 spikes due to seasonal demand.")
    print("2. Miami consistently performs as a top location, while Jacksonville tends to generate lower total sales.")
    print("3. Electronics has the strongest category performance across most locations.")
    print("4. There is a positive relationship between advertising spend and sales, suggesting marketing investment supports revenue growth.")
    print("5. Customer age profiles vary by location, which can help tailor local marketing strategies.")
    print("6. Mid-range and premium tiers contribute a meaningful share of sales, indicating value in maintaining diverse pricing options.")

    print("\nBUSINESS RECOMMENDATIONS:")
    print("1. Increase inventory and marketing ahead of Q4 to maximize seasonal demand.")
    print("2. Study Miami's performance to identify strategies that can be replicated in lower-performing stores.")
    print("3. Continue prioritizing Electronics while improving performance in weaker categories.")
    print("4. Optimize advertising budgets toward channels and periods with stronger sales efficiency.")
    print("5. Use location-specific customer age trends to personalize promotions and merchandising.")

    # Display all figures
    plt.show()


# Run the main function
if __name__ == "__main__":
    main()