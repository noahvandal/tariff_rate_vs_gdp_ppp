import pandas as pd
import requests

def extract_tariff_table():
    # URL of the Wikipedia page
    url = 'https://en.wikipedia.org/wiki/List_of_countries_by_tariff_rate'
    
    try:
        # Read all tables from the Wikipedia page
        tables = pd.read_html(url)
        
        # The main tariff table is the one with the most rows and contains country data
        main_table = None
        for table in tables:
            if len(table.columns) >= 7:  # Table should have at least 7 columns
                if 'Country/Territory/Region/Group' in table.columns[0]:  # Check first column name
                    main_table = table
                    break
        
        if main_table is None:
            raise ValueError("Could not find the tariff rate table")
        
        # Clean up the data
        # Remove rows that contain 'Notes:' or 'References'
        main_table = main_table[~main_table.iloc[:, 0].str.contains('Notes:|References', na=False, regex=True)]
        
        # The column names are multi-level, so we'll simplify them
        main_table.columns = [
            'Country',
            'WB_Rate',
            'WB_Year',
            'WTO_Rate',
            'WTO_Year',
            'UNCTAD_Rate',
            'UNCTAD_Year'
        ]
        
        # Convert rate columns to numeric, removing '%' signs
        rate_columns = ['WB_Rate', 'WTO_Rate', 'UNCTAD_Rate']
        for col in rate_columns:
            main_table[col] = pd.to_numeric(
                main_table[col].str.replace('%', '').str.replace('—', 'NaN'),
                errors='coerce'
            )
        
        # Save to CSV
        main_table.to_csv('tariff_rates.csv', index=False)
        
        return main_table
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

if __name__ == "__main__":
    # Extract and display the table
    tariff_data = extract_tariff_table()
    if tariff_data is not None:
        print("Successfully extracted tariff data!")
        print("\nFirst few rows of the data:")
        print(tariff_data.head())
        print(f"\nTotal number of countries/regions: {len(tariff_data)}")
