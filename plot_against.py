import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os
import seaborn as sns
import numpy as np

def create_scatter_plot():
    # Read the CSV files
    gdp_data = pd.read_csv('gdp_ppp_per_capita.csv')
    tariff_data = pd.read_csv('tariff_rates.csv')
    
    # Clean up country names
    gdp_data['Country'] = gdp_data['Country'].str.replace('*', '').str.strip()
    tariff_data['Country'] = tariff_data['Country'].str.strip()
    
    # Remove 'WORLD' and any regional groupings from tariff data
    tariff_data = tariff_data[~tariff_data['Country'].isin(['WORLD', 'European Union'])]
    
    # Clean up the GDP data
    for col in gdp_data.columns:
        if 'Value' in col:
            gdp_data[col] = pd.to_numeric(gdp_data[col].astype(str).str.replace('%', '').str.replace(',', ''), errors='coerce')
    
    # Clean up the tariff data
    tariff_data['WB_Rate'] = pd.to_numeric(tariff_data['WB_Rate'].astype(str).str.replace('%', ''), errors='coerce')
    
    # Create a merged dataset
    merged_data = pd.merge(gdp_data, tariff_data, on='Country', how='inner')
    
    # Use CIA data for GDP, falling back to IMF if CIA is not available
    merged_data['GDP_PPP'] = merged_data['CIA_Value'].fillna(merged_data['IMF_Value'])
    
    # Remove any rows where either GDP or Tariff rate is missing
    merged_data = merged_data.dropna(subset=['GDP_PPP', 'WB_Rate'])
    
    # Create the figure with XKCD style
    with plt.xkcd(scale=1, length=100, randomness=2):  # Adjusted XKCD parameters
        # Create new figure with white background
        fig = plt.figure(figsize=(12, 8), facecolor='white')
        ax = fig.add_subplot(111)
        ax.set_facecolor('white')
        
        # Create scatter plot
        sns.scatterplot(data=merged_data, x='WB_Rate', y='GDP_PPP', alpha=0.6, ax=ax)
        
        # Add labels for some interesting points
        for idx, row in merged_data.iterrows():
            if row['GDP_PPP'] > 80000 or row['WB_Rate'] > 15:
                ax.annotate(row['Country'], 
                          (row['WB_Rate'], row['GDP_PPP']),
                          xytext=(5, 5), textcoords='offset points',
                          fontsize=8)
        
        # Add title and labels
        ax.set_title('Do Higher Tariffs = Lower GDP?', fontsize=14, pad=20)
        ax.set_xlabel('Tariff Rate (%)', fontsize=12)
        ax.set_ylabel('GDP per Capita (PPP, $)', fontsize=12)
        
        # Add a trend line
        z = np.polyfit(merged_data['WB_Rate'], merged_data['GDP_PPP'], 1)
        p = np.poly1d(z)
        plt.plot(merged_data['WB_Rate'], p(merged_data['WB_Rate']), "r--", alpha=0.8)
        
        # Calculate correlation coefficient and R-squared
        correlation = merged_data['WB_Rate'].corr(merged_data['GDP_PPP'])
        r_squared = correlation ** 2
        plt.text(0.8, 0.95, f'Correlation: {correlation:.2f}\nR²: {r_squared:.2f}', 
                transform=ax.transAxes, fontsize=10)
        
        # Add grid lines
        ax.grid(True, alpha=0.3)
        
        # Adjust layout
        plt.tight_layout()
        
        # Save the plot with white background
        plt.savefig('gdp_vs_tariff.png', dpi=300, bbox_inches='tight', 
                    facecolor='white', edgecolor='none')
        plt.close()
    
    # Print statistics
    print(f"Number of countries in analysis: {len(merged_data)}")
    print(f"\nCorrelation coefficient: {correlation:.3f}")
    print("\nTop 5 countries by GDP (PPP) per capita:")
    print(merged_data.nlargest(5, 'GDP_PPP')[['Country', 'GDP_PPP', 'WB_Rate']])
    print("\nTop 5 countries by Tariff Rate:")
    print(merged_data.nlargest(5, 'WB_Rate')[['Country', 'GDP_PPP', 'WB_Rate']])

if __name__ == "__main__":
    create_scatter_plot()
