#!/opt/anaconda3/bin/python3

import pandas as pd
from datetime import datetime, timedelta
import re
from FuzzyDateParser import FuzzyDateParser



def load_checkout_data(file_path):
    try:
        df = pd.read_excel(file_path)
        print("Excel file loaded successfully.")
        return df
    except Exception as e:
        print(f"Failed to load file: {e}")
        return None


def inspect_rows(df):
    print(f"\nDataFrame loaded with {len(df)} rows.\n")

    while True:
        index = input("enter row number to inspect or type a letter to exit: ").strip()
        if not index.isdigit():
            print("Exiting inspection.")
            break
        else:
            try:
                i = int(index)
                if 0 <= i < len(df):
                    print("\n=== ROW {} ===".format(i))
                    print(df.iloc[i])
                    print("")
                else:
                    print(f"Row {i} is out of range. Try 1 to {len(df)}.\n")
            except ValueError:
                print("Invalid input. Please enter a number.\n")


def inspect_unique_values(df):
    unique_values = df['Date Due'].dropna().unique()
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