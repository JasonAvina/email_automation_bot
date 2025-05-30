#!/opt/anaconda3/bin/python3

import pandas as pd
from datetime import datetime, timedelta
import re
from parse_fuzzy_date import FuzzyDateParser



def load_checkout_data(file_path):
    """Load Excel file into a pandas DataFrame."""
    try:
        df = pd.read_excel(file_path)
        print("Excel file loaded successfully.")
        return df
    except Exception as e:
        print(f"Failed to load file: {e}")
        return None

def inspect_rows(df):
    print(f"\nDataFrame loaded with {len(df)} rows.")
    print("Enter a row number to inspect it. Enter '0' to quit.\n")

    while True:
        index = input("Row number (1-based): ").strip()
        if index == '0':
            print("Exiting inspection.")
            break
        try:
            i = int(index) - 1
            if 0 <= i < len(df):
                print("\n=== ROW {} ===".format(i + 1))
                print(df.iloc[i])
                print("")
            else:
                print(f"Row {i + 1} is out of range. Try 1 to {len(df)}.\n")
        except ValueError:
            print("Invalid input. Please enter a number.\n")

def inspect_unique_values(df):
    unique_values = df['Expected Return Date'].dropna().unique()
    print(f"\nFound {len(unique_values)} unique values in 'Expected Return Date':\n")
    datetimes = {}
    nondatetimes = {}
    for i, val in enumerate(unique_values, 1):
        if isinstance(val, datetime):  # Just 'datetime', not 'datetime.datetime'
            datetimes[i] = val
        else:
            nondatetimes[i] = val
    
    for key, value in datetimes.items():
        print(f"{key} -> {value}")
    for key, value in nondatetimes.items():
        print(f"{key} -> {value}")
 
def parse_row(row):
    parser = FuzzyDateParser()
    value = row['Expected Return Date']
    base = row['Date'] if isinstance(row['Date'], (datetime, pd.Timestamp)) else None
    return parser.parse(value, base_date=base)


def print_overdue_rows(df):
    today = datetime.today().date()
    overdue = df[(df['Parsed Return Date'].notna()) & (df['Parsed Return Date'] < today)]

    print("\n=== OVERDUE CHECKOUTS ===")
    if overdue.empty:
        print("No overdue checkouts found.")
    else:
        print(overdue[['Expected Return Date', 'Date', 'Parsed Return Date']])



# ------------------------------
# Main Logic
# ------------------------------
if __name__ == "__main__":

    FILE_PATH = "LIB 80 Equipment Checkouts.xlsx"
    df = load_checkout_data(FILE_PATH)

    inspect = input('would you like to inspect the data before parsing?').lower().strip()
    if inspect == 'yes':
        print(df.head())
        inspect_rows(df)
        inspect_unique_values(df)

    if df is not None:
        df['Parsed Return Date'] = df.apply(parse_row, axis=1)
    
    print_overdue_rows(df)

