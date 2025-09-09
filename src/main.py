# src/main.py

import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
import os
import time
from pathlib import Path
from pandas.api.types import is_numeric_dtype, is_bool_dtype

from scraper import get_escooter_data
from data_processor import process_dataframe
from filter_sort import filter_by_numeric, filter_by_categorical, sort_by_column

# --- Configuration ---
ESCOOTER_URL = "https://www.escooter-treff.de/tabelle/"
CONSOLE = Console()
CACHE_FILE = Path("data/escooter_data.csv") # Store data in a dedicated folder
CACHE_DURATION_SECONDS = 24 * 60 * 60 # 24 hours


def display_dataframe(df: pd.DataFrame, title: str = "E-Scooter Data"):
    """Displays a pandas DataFrame using rich.table."""
    if df.empty:
        CONSOLE.print("[yellow]No data to display. Your filters might be too restrictive.[/yellow]")
        return
        
    rich_table = Table(title=title, show_header=True, header_style="bold magenta")
    
    for column in df.columns:
        rich_table.add_column(column)
        
    for _, row in df.iterrows():
        rich_table.add_row(*[str(item) if pd.notna(item) else "" for item in row])
        
    CONSOLE.print(rich_table)

def load_data() -> pd.DataFrame:
    """
    Loads data from cache if it's recent, otherwise scrapes from the web
    and updates the cache.
    """
    CACHE_FILE.parent.mkdir(exist_ok=True)

    if CACHE_FILE.exists():
        file_mod_time = CACHE_FILE.stat().st_mtime
        if (time.time() - file_mod_time) < CACHE_DURATION_SECONDS:
            CONSOLE.print(f"[bold green]✓ Loading data from local cache...[/bold green]")
            return pd.read_csv(CACHE_FILE)

    CONSOLE.print("[bold yellow]Cache old or missing. Scraping fresh data from the web...[/bold yellow]")
    with CONSOLE.status("[bold green]Scraping and processing...[/bold green]"):
        raw_data = get_escooter_data(ESCOOTER_URL)
    
    if 'current' in raw_data:
        df = process_dataframe(raw_data['current'])
        df.to_csv(CACHE_FILE, index=False)
        CONSOLE.print(f"[bold green]✓ Success![/bold green] Saved fresh data to cache.")
        return df
    else:
        CONSOLE.print("[bold red]✗ Error:[/bold red] Could not retrieve e-scooter data.")
        return pd.DataFrame()

def main_menu(df_original: pd.DataFrame):
    """The main interactive loop for filtering and sorting."""
    df_current = df_original.copy()

    while True:
        CONSOLE.print("\n[bold cyan]E-Scooter Analyzer Menu[/bold cyan]")
        CONSOLE.print("[1] Filter Data")
        CONSOLE.print("[2] Sort Data")
        CONSOLE.print("[3] Display Current List")
        CONSOLE.print("[4] Reset to Full List")
        CONSOLE.print("[5] Exit")
        
        choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5"], default="3")

        if choice == '1': # Filter
            for i, col in enumerate(df_current.columns):
                CONSOLE.print(f"  [{i}] {col} ({df_current[col].dtype})")
            
            col_index = int(Prompt.ask("Enter the number of the column to filter by"))
            column_name = df_current.columns[col_index]

            # --- THIS IS THE FIX ---
            # Check if the column is numeric BUT NOT boolean
            if is_numeric_dtype(df_current[column_name]) and not is_bool_dtype(df_current[column_name]):
                op = Prompt.ask(f"Filter '{column_name}' | Enter operator", choices=['<', '<=', '>', '>=', '=='], default='<=')
                val = float(Prompt.ask("Enter value"))
                df_current = filter_by_numeric(df_current, column_name, op, val)
            else: # This block now correctly handles Boolean, Object, and Category types
                options = sorted(df_current[column_name].dropna().unique().tolist())
                
                CONSOLE.print(f"Available options for '{column_name}':")
                for i, option in enumerate(options):
                    CONSOLE.print(f"  [{i}] {option}")
                
                indices_str = Prompt.ask("Enter the numbers of the options to INCLUDE (e.g., '0, 2')")
                indices = indices_str.replace(" ", "").split(',')
                try:
                    selected = [options[int(i)] for i in indices if i]
                    df_current = filter_by_categorical(df_current, column_name, selected)
                except (ValueError, IndexError):
                    CONSOLE.print("[red]Invalid selection.[/red]")

            display_dataframe(df_current)

        elif choice == '2': # Sort
            for i, col in enumerate(df_current.columns):
                CONSOLE.print(f"  [{i}] {col}")
            col_index = int(Prompt.ask("Enter the number of the column to sort by"))
            column_name = df_current.columns[col_index]

            order = Prompt.ask("Sort order", choices=['asc', 'desc'], default='asc')
            df_current = sort_by_column(df_current, column_name, ascending=(order == 'asc'))
            display_dataframe(df_current)

        elif choice == '3': # Display
            display_dataframe(df_current)

        elif choice == '4': # Reset
            df_current = df_original.copy()
            CONSOLE.print("[green]Filters and sorting have been reset.[/green]")
            display_dataframe(df_current)

        elif choice == '5': # Exit
            CONSOLE.print("[bold]Goodbye![/bold]")
            break

if __name__ == "__main__":
    df = load_data()
    
    if not df.empty:
        CONSOLE.print(f"Loaded {len(df)} e-scooters.")
        main_menu(df)
    else:
        CONSOLE.print("[bold red]Could not load any data to analyze.[/bold red]")