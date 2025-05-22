# checkout_bot.py

import pandas as pd

# File path (assumes the file is in the same directory as this script)
EXCEL_FILE = "LIB 80 Equipment Checkouts.xlsx"

def load_checkout_data(file_path):
    """Load the Excel file into a pandas DataFrame."""
    try:
        df = pd.read_excel(file_path)
        print("File loaded successfully.")
        return df
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    df = load_checkout_data(EXCEL_FILE)
    
    if df is not None:
        print(df.head())  # Show the first few rows
