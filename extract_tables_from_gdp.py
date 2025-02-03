import pandas as pd
import requests

def extract_gdp_ppp_table():
    # URL of the Wikipedia page
    url = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(PPP)_per_capita'
    
    try:
        # Read all tables from the Wikipedia page
        tables = pd.read_html(url)
        
        # The main GDP table is typically the one with country data and multiple columns for different sources
        main_table = None
        for table in tables:
            if 'Country/Territory' in str(table.columns) and 'IMF' in str(table.columns):
                main_table = table
                break
        
        if main_table is None:
            raise ValueError("Could not find the GDP (PPP) per capita table")
        
        # Clean up the data
        # Convert all columns to string type first
        for col in main_table.columns:
            main_table[col] = main_table[col].astype(str)
        
        # Remove rows that contain notes or references
        main_table = main_table[~main_table.iloc[:, 0].str.contains('Notes|References|Footnotes', na=False, regex=True)]
        
        # Rename columns for clarity
        main_table.columns = [
            'Country',
            'IMF_Value',
            'IMF_Year',
            'World_Bank_Value',
            'World_Bank_Year',
            'CIA_Value',
            'CIA_Year'
        ]
        
        # Convert value columns to numeric, removing currency symbols and commas
        value_columns = ['IMF_Value', 'World_Bank_Value', 'CIA_Value']
        for col in value_columns:
            main_table[col] = pd.to_numeric(
                main_table[col].str.replace('$', '').str.replace(',', '').str.replace('—', 'NaN'),
                errors='coerce'
            )
        
        # Save to CSV
        main_table.to_csv('gdp_ppp_per_capita.csv', index=False)
        
        return main_table
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

if __name__ == "__main__":
    # Extract and display the table
    gdp_data = extract_gdp_ppp_table()
    if gdp_data is not None:
        print("Successfully extracted GDP (PPP) per capita data!")
        print("\nFirst few rows of the data:")
        print(gdp_data.head())
        print(f"\nTotal number of countries/territories: {len(gdp_data)}")