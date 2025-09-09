# src/data_processor.py

import pandas as pd
import re
import numpy as np

def clean_column_name(col_name: str) -> str:
    """Cleans column names for better DataFrame usability."""
    col_name = col_name.replace('eScooter', 'Model')
    # Keeping units as requested
    col_name = col_name.replace('*', '').replace('(', '').replace(')', '').strip()
    col_name = col_name.replace(' ', '_').lower()
    return col_name

def parse_numeric_value(value: str) -> float | None:
    """
    Parses a string to extract a numeric value, handling units, ranges, and special formats.
    """
    if not isinstance(value, str):
        return None
    
    value = value.replace(',', '.')
    
    # Handle '2x250' format for motor power by multiplying
    if 'x' in value and len(re.findall(r"(\d+(\.\d+)?)", value)) > 1:
        parts = value.lower().split('x')
        try:
            return float(parts[0]) * float(re.findall(r"(\d+(\.\d+)?)", parts[1])[0][0])
        except (ValueError, IndexError):
            pass # Fallback to standard parsing

    numbers = re.findall(r"(\d+(\.\d+)?)", value)
    if numbers:
        return float(numbers[0][0])
    
    return None

def process_dataframe(raw_data: list[list[str]]) -> pd.DataFrame:
    """
    Converts raw list of lists into a cleaned pandas DataFrame.
    """
    if not raw_data or len(raw_data) < 2:
        return pd.DataFrame()

    df = pd.DataFrame(raw_data[1:], columns=raw_data[0])
    
    df.columns = [clean_column_name(col) for col in df.columns]

    # Dynamically find columns that seem numeric based on their name
    numeric_keywords = ['kg', 'km', 'wh', 'volt', 'ah', 'w', 'zollgröße', 'bis_kg', 'uvp']
    
    # Loop through all columns to clean and type-cast them
    for col in df.columns:
        # Booleans
        if 'toleranz_optimiert' in col or 'bremslicht' in col or 'wechselakku' in col:
            df[col] = df[col].apply(lambda x: 'ja' in str(x).lower() or '✓' in str(x))
            continue
            
        # Blinker count
        if 'blinker' in col:
            df[col] = df[col].apply(lambda x: parse_numeric_value(x) if x else 0).fillna(0).astype(int)
            continue

        # Check if any keyword matches to identify as numeric
        if any(keyword in col for keyword in numeric_keywords):
            df[col] = df[col].apply(parse_numeric_value)
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Drop the coupon code column if it exists, as it's not useful for analysis
    if 'gutscheincode_werbung' in df.columns:
        df = df.drop(columns=['gutscheincode_werbung'])

    return df

# Example usage for verification
if __name__ == "__main__":
    from scraper import get_escooter_data
    ESCOOTER_URL = "https://www.escooter-treff.de/tabelle/"

    raw_data = get_escooter_data(ESCOOTER_URL)

    if 'current' in raw_data:
        print("\n--- Processing Current Models (Revised) ---")
        df_current = process_dataframe(raw_data['current'])
        print(df_current.head())
        print("\nDataFrame Info (Current Models):")
        df_current.info()