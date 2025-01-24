import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns
import os

# File paths
DATA_PATH = 'c:/Users/paulb/CascadeProjects/SECthingv2/analysis/data/original_xrt_data.csv'
OUTPUT_PATH = 'c:/Users/paulb/CascadeProjects/SECthingv2/analysis/reports/'
VIZ_PATH = 'c:/Users/paulb/CascadeProjects/SECthingv2/analysis/visualizations/'

def load_data():
    """Load and perform initial data cleaning"""
    df = pd.read_csv(DATA_PATH)
    return df

def clean_data(df):
    """Clean and preprocess the data"""
    # Replace 'nan' strings with actual NaN
    df = df.replace('nan', np.nan)
    
    # Convert date columns
    date_columns = ['Event timestamp', 'Execution Timestamp', 'Effective Date', 'Expiration Date']
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    
    return df

def analyze_outliers(df):
    """Analyze numerical outliers in the dataset"""
    outlier_report = {}
    
    # Function to detect outliers using IQR method
    def get_outliers(series, column_name):
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = series[(series < lower_bound) | (series > upper_bound)]
        return {
            'column': column_name,
            'outliers': outliers,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'Q1': Q1,
            'Q3': Q3
        }

    # Analyze notional amounts by currency
    print("\nAnalyzing notional amounts...")
    for currency in df['Notional currency-Leg 1'].unique():
        if pd.isna(currency):
            continue
        mask = df['Notional currency-Leg 1'] == currency
        notional = pd.to_numeric(df[mask]['Notional amount-Leg 1'].str.replace(',', ''), errors='coerce')
        if not notional.empty:
            outlier_report[f'notional_{currency}'] = get_outliers(notional, f'Notional Amount ({currency})')

    # Analyze prices
    print("Analyzing prices...")
    prices = pd.to_numeric(df['Price'].str.replace(',', ''), errors='coerce')
    outlier_report['prices'] = get_outliers(prices, 'Price')

    # Analyze quantities
    print("Analyzing quantities...")
    quantities = pd.to_numeric(df['Total notional quantity-Leg 1'].str.replace(',', ''), errors='coerce')
    outlier_report['quantities'] = get_outliers(quantities, 'Quantity')

    # Analyze price/quantity ratios
    print("Analyzing price/quantity ratios...")
    df['price_quantity_ratio'] = prices / quantities
    ratios = df['price_quantity_ratio'].dropna()
    outlier_report['price_quantity_ratios'] = get_outliers(ratios, 'Price/Quantity Ratio')

    # Generate outlier report
    generate_outlier_report(outlier_report)
    
    return outlier_report

def generate_outlier_report(outlier_report):
    """Generate a detailed report of the outliers"""
    report_path = 'c:/Users/paulb/CascadeProjects/SECthingv2/analysis/reports/outlier_analysis.md'
    
    # Create reports directory if it doesn't exist
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, 'w') as f:
        f.write("# XRT Trading Data Outlier Analysis\n\n")
        f.write(f"Analysis generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        for category, data in outlier_report.items():
            f.write(f"## {data['column']}\n\n")
            f.write(f"- Number of outliers: {len(data['outliers'])}\n")
            f.write(f"- Range boundaries:\n")
            f.write(f"  - Lower bound: {data['lower_bound']:.2f}\n")
            f.write(f"  - Upper bound: {data['upper_bound']:.2f}\n")
            f.write(f"- Distribution:\n")
            f.write(f"  - Q1: {data['Q1']:.2f}\n")
            f.write(f"  - Q3: {data['Q3']:.2f}\n\n")
            
            if not data['outliers'].empty:
                f.write("### Top Outliers:\n")
                sorted_outliers = data['outliers'].sort_values()
                f.write("Lowest values:\n")
                for idx, value in sorted_outliers.head().items():
                    f.write(f"- ID {idx}: {value:.2f}\n")
                f.write("\nHighest values:\n")
                for idx, value in sorted_outliers.tail().items():
                    f.write(f"- ID {idx}: {value:.2f}\n")
            f.write("\n---\n\n")

def analyze_currencies(df):
    """Analyze currency distribution and patterns"""
    # Add currency analysis logic here
    pass

def analyze_jpy_trades(df):
    """Detailed analysis of JPY trades"""
    # Filter for JPY trades
    jpy_trades = df[df['Notional currency-Leg 1'] == 'JPY'].copy()
    
    # Convert notional amount to numeric, removing commas
    jpy_trades['Notional_Amount_Numeric'] = pd.to_numeric(
        jpy_trades['Notional amount-Leg 1'].str.replace(',', ''), 
        errors='coerce'
    )
    
    # Calculate statistics for outlier detection
    Q1 = jpy_trades['Notional_Amount_Numeric'].quantile(0.25)
    Q3 = jpy_trades['Notional_Amount_Numeric'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Identify outliers
    outliers = jpy_trades[
        (jpy_trades['Notional_Amount_Numeric'] < lower_bound) | 
        (jpy_trades['Notional_Amount_Numeric'] > upper_bound)
    ]
    
    # Sort outliers by notional amount
    outliers = outliers.sort_values('Notional_Amount_Numeric', ascending=False)
    
    # Generate detailed report
    report_path = 'c:/Users/paulb/CascadeProjects/SECthingv2/analysis/reports/jpy_trades_analysis.md'
    
    with open(report_path, 'w') as f:
        f.write("# JPY Trades Analysis\n\n")
        f.write(f"Analysis generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Overall statistics
        f.write("## Overall Statistics\n\n")
        f.write(f"- Total JPY trades: {len(jpy_trades)}\n")
        f.write(f"- Number of outliers: {len(outliers)}\n")
        f.write(f"- Normal range: {lower_bound:,.2f} to {upper_bound:,.2f} JPY\n")
        f.write(f"- Q1: {Q1:,.2f} JPY\n")
        f.write(f"- Q3: {Q3:,.2f} JPY\n\n")
        
        # Detailed outlier analysis
        f.write("## Outlier Trades\n\n")
        for idx, trade in outliers.iterrows():
            f.write(f"### Trade Details (Dissemination ID: {trade['Dissemination Identifier']})\n\n")
            f.write(f"- **Notional Amount:** {trade['Notional_Amount_Numeric']:,.2f} JPY\n")
            f.write(f"- **Action Type:** {trade['Action type']}\n")
            f.write(f"- **Event Type:** {trade['Event type']}\n")
            f.write(f"- **Event Timestamp:** {trade['Event timestamp']}\n")
            f.write(f"- **Execution Timestamp:** {trade['Execution Timestamp']}\n")
            f.write(f"- **Effective Date:** {trade['Effective Date']}\n")
            f.write(f"- **Expiration Date:** {trade['Expiration Date']}\n")
            f.write(f"- **Price:** {trade['Price']}\n")
            f.write(f"- **Quantity:** {trade['Total notional quantity-Leg 1']}\n")
            f.write(f"- **Platform:** {trade['Platform identifier']}\n")
            f.write(f"- **Original Dissemination ID:** {trade['Original Dissemination Identifier']}\n")
            f.write(f"- **ISIN:** {trade['Underlier ID-Leg 1']}\n")
            f.write("\n---\n\n")
    
    return outliers

def generate_visualizations(df):
    """Create visualizations of key metrics"""
    # Create directory if it doesn't exist
    os.makedirs(VIZ_PATH, exist_ok=True)

    # Box plots for numerical columns
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=pd.to_numeric(df['Price'].str.replace(',', ''), errors='coerce'))
    plt.title('Price Distribution with Outliers')
    plt.savefig(os.path.join(VIZ_PATH, 'price_boxplot.png'))
    plt.close()

    # Scatter plot of price vs quantity
    plt.figure(figsize=(12, 6))
    plt.scatter(
        pd.to_numeric(df['Total notional quantity-Leg 1'].str.replace(',', ''), errors='coerce'),
        pd.to_numeric(df['Price'].str.replace(',', ''), errors='coerce'),
        alpha=0.5
    )
    plt.xlabel('Quantity')
    plt.ylabel('Price')
    plt.title('Price vs Quantity Scatter Plot')
    plt.savefig(os.path.join(VIZ_PATH, 'price_quantity_scatter.png'))
    plt.close()

    # JPY-specific visualizations
    jpy_trades = df[df['Notional currency-Leg 1'] == 'JPY'].copy()
    if not jpy_trades.empty:
        # Convert notional amount to numeric
        jpy_trades['Notional_Amount_Numeric'] = pd.to_numeric(
            jpy_trades['Notional amount-Leg 1'].str.replace(',', ''), 
            errors='coerce'
        )
        
        # Notional amount distribution
        plt.figure(figsize=(12, 6))
        sns.histplot(data=jpy_trades, x='Notional_Amount_Numeric', bins=30)
        plt.title('Distribution of JPY Notional Amounts')
        plt.xlabel('Notional Amount (JPY)')
        plt.ylabel('Count')
        plt.ticklabel_format(style='plain', axis='x')
        plt.savefig(os.path.join(VIZ_PATH, 'jpy_notional_distribution.png'))
        plt.close()
        
        # Timeline of JPY trades
        plt.figure(figsize=(15, 6))
        plt.scatter(
            pd.to_datetime(jpy_trades['Event timestamp']),
            jpy_trades['Notional_Amount_Numeric'],
            alpha=0.6
        )
        plt.title('Timeline of JPY Trades')
        plt.xlabel('Event Timestamp')
        plt.ylabel('Notional Amount (JPY)')
        plt.xticks(rotation=45)
        plt.ticklabel_format(style='plain', axis='y')
        plt.tight_layout()
        plt.savefig(os.path.join(VIZ_PATH, 'jpy_trades_timeline.png'))
        plt.close()

def main():
    # Load data
    print("Loading data...")
    df = load_data()
    
    # Clean data
    print("Cleaning data...")
    df = clean_data(df)
    
    # Perform outlier analysis
    print("Analyzing outliers...")
    outlier_report = analyze_outliers(df)
    
    # Perform detailed JPY analysis
    print("Analyzing JPY trades...")
    jpy_outliers = analyze_jpy_trades(df)
    
    # Generate visualizations
    print("Generating visualizations...")
    generate_visualizations(df)
    
    print("\nAnalysis complete! Check the reports and visualizations directories for results.")

if __name__ == "__main__":
    main()
