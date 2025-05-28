#!/opt/anaconda3/bin/python3

import pandas as pd
from datetime import datetime, timedelta
import re


# ------------------------------
# Load the Excel file
# ------------------------------
def load_checkout_data(file_path):
    """Load Excel file into a pandas DataFrame."""
    try:
        df = pd.read_excel(file_path)
        print("Excel file loaded successfully.")
        return df
    except Exception as e:
        print(f"Failed to load file: {e}")
        return None


# ------------------------------
# Parse fuzzy employee-entered date strings
# ------------------------------
def parse_fuzzy_date(value):
    # Get today's date
    today = datetime.today().date()

    # If expected return date is a DATETIME
    if isinstance(value, (datetime, pd.Timestamp)):
        return value.date()
    
    # If expected return date is a STRING
    elif isinstance(value, str):
        val = value.strip().lower()
        if val in ("eod", "end of day"):
            return today
        elif val in ("tomorrow", "tmrw"):
            return today + timedelta(days=1)
        elif val in ("end of week", "eow"):
            days_ahead = 4 - today.weekday()  # Friday is 4
            if days_ahead <= 0:  # If today is Friday or weekend
                days_ahead += 7
            return today + timedelta(days=days_ahead)
        elif "monday" in val:
            days_ahead = 0 - today.weekday()  # Monday is 0
            if days_ahead <= 0:  # Target day already happened this week
                days_ahead += 7
            return today + timedelta(days=days_ahead)
        elif "friday" in val:
            days_ahead = 4 - today.weekday()  # Friday is 4
            if days_ahead <= 0:  # Target day already happened this week
                days_ahead += 7
            return today + timedelta(days=days_ahead)
        elif re.match(r"\d{1,2}/\d{1,2}/\d{2,4}", val):
            try:
                parsed_date = pd.to_datetime(val, errors="coerce")
                return parsed_date.date() if not pd.isna(parsed_date) else pd.NaT
            except:
                return pd.NaT
        else:
            return pd.NaT
    else:
        return pd.NaT


# ------------------------------
# Add parsed return dates to the DataFrame
# ------------------------------
def add_parsed_return_dates(df):
    df['Parsed Return Date'] = df['Expected Return Date'].apply(parse_fuzzy_date)


# ------------------------------
# Interactive Row Inspection Loop
# ------------------------------
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

# ------------------------------
# print unique values
# ------------------------------

def print_unique_return_dates(df):
    unique_values = df['Expected Return Date'].dropna().unique()
    print(f"\nFound {len(unique_values)} unique values in 'Expected Return Date':\n")
    for i, val in enumerate(unique_values, 1):
        if not isinstance(val, datetime):  # Just 'datetime', not 'datetime.datetime'
            print(f"{i}. {val}")


# ------------------------------
# Main Logic
# ------------------------------
if __name__ == "__main__":

    FILE_PATH = "LIB 80 Equipment Checkouts.xlsx"
    df = load_checkout_data(FILE_PATH)

    if df is not None:
        add_parsed_return_dates(df)
        inspect_rows(df)
        print_unique_return_dates(df)

