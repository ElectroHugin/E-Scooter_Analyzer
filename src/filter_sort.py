# src/filter_sort.py

import pandas as pd
from pandas.api.types import is_numeric_dtype

def filter_by_numeric(df: pd.DataFrame, column: str, operator: str, value: float) -> pd.DataFrame:
    """Filters a DataFrame on a numeric column."""
    if column not in df.columns or not is_numeric_dtype(df[column]):
        print(f"Warning: Column '{column}' is not a valid numeric column.")
        return df

    if operator == '<':
        return df[df[column] < value]
    elif operator == '<=':
        return df[df[column] <= value]
    elif operator == '>':
        return df[df[column] > value]
    elif operator == '>=':
        return df[df[column] >= value]
    elif operator == '==':
        return df[df[column] == value]
    else:
        print(f"Warning: Invalid operator '{operator}'.")
        return df

def filter_by_categorical(df: pd.DataFrame, column: str, values: list) -> pd.DataFrame:
    """Filters a DataFrame on a categorical/string column."""
    if column not in df.columns:
        print(f"Warning: Column '{column}' not found.")
        return df
    
    return df[df[column].isin(values)]

def sort_by_column(df: pd.DataFrame, column: str, ascending: bool = True) -> pd.DataFrame:
    """Sorts a DataFrame by a specific column."""
    if column not in df.columns:
        print(f"Warning: Column '{column}' not found.")
        return df
    
    return df.sort_values(by=column, ascending=ascending)