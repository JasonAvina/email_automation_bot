#!/opt/anaconda3/bin/python3

import pandas as pd
from datetime import datetime, timedelta
import re
from FuzzyDateParser import FuzzyDateParser



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

def print_overdue_rows(df):
    today = datetime.today().date()
    overdue = df[(df['Parsed Return Date'].notna()) & (df['Parsed Return Date'] < today)]

    print("\n=== OVERDUE CHECKOUTS ===")
    if overdue.empty:
        print("No overdue checkouts found.")
    else:
        print(overdue[['Expected Return Date', 'Date', 'Parsed Return Date']])

def check_for_overdue(df):
    today = datetime.today().date()
    overdue_indices = []
    for index, row in df.iterrows():
        if row['Parsed Return Date'] is not None and row['Parsed Return Date'] < today:
            overdue_indices.append(index)
    return overdue_indices

def print_overdue(df, overdue_indices):
    today = datetime.today().date()
    print(f"\nToday's date: {today}")
    print("Press Enter to view the next overdue row, type a row number to jump to it, or 'q' to quit.\n")

    position = 0
    while 0 <= position < len(overdue_indices):
        index = overdue_indices[position]
        row = df.loc[index]
        parsed_date = row['Parsed Return Date']
        estimated_excel_row = index + 2  # 0-indexed + header row

        print(f"\n=== OVERDUE ROW {index} (est. Excel row {estimated_excel_row}) ({position + 1} of {len(overdue_indices)}) ===")
        print(row.to_string())
        print("\n--- Key Dates ---")
        print(f"Checkout Date:        {row.get('Date', 'N/A')}")
        print(f"Expected Return Date: {row.get('Expected Return Date', 'N/A')}")
        print(f"Parsed Return Date:   {parsed_date}")
        print("-" * 60)

        user_input = input("Next [Enter] | Jump to row [number] | Quit [q]: ").strip().lower()
        if user_input == 'q':
            print("Exiting overdue review.")
            break
        elif user_input.isdigit():
            pos = int(user_input) - 1
            if 0 <= pos < len(overdue_indices):
                position = pos
            else:
                print(f"Invalid row number. Must be between 1 and {len(overdue_indices)}.")
        else:
            position += 1





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
        parser = FuzzyDateParser(df)
        parser.df['Parsed Return Date'] = parser.df.apply(parser.parse_row, axis=1)
        overdue_list = check_for_overdue(parser.df)
        print_overdue(parser.df, overdue_list)

    
    
    print_overdue_rows(df)

