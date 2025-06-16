#!/opt/anaconda3/bin/python3

import pandas as pd
from datetime import datetime, timedelta
import re
from FuzzyDateParser import FuzzyDateParser



def load_checkout_data(file_path):
    try:
        df = pd.read_excel(file_path)
        df.index = df.index + 1  # Change index to start at 1
        print("Excel file loaded successfully.")
        return df
    except Exception as e:
        print(f"Failed to load file: {e}")
        return None


def inspect_rows(df):
    print(f"\nDataFrame loaded with {len(df)} rows.\n")
    print("Enter a row number to inspect it. Enter '0' to quit.\n")

    while True:
        index = input("Type 0 to exit or enter row number to inspect: ").strip()
        if index == '0':
            print("Exiting inspection.")
            break
        try:
            i = int(index)
            if 0 < i < len(df):
                print("\n=== ROW {} ===".format(i + 1))
                print(df.iloc[i])
                print("")
            else:
                print(f"Row {i} is out of range. Try 1 to {len(df)}.\n")
        except ValueError:
            print("Invalid input. Please enter a number.\n")

# # def inspect_unique_values(df):
#     unique_values = df['Expected Return Date'].dropna().unique()
#     print(f"\nFound {len(unique_values)} unique values in 'Expected Return Date':\n")
#     datetimes = {}
#     nondatetimes = {}
#     for i, val in enumerate(unique_values, 1):
#         if isinstance(val, datetime):  # Just 'datetime', not 'datetime.datetime'
#             datetimes[i] = val
#         else:
#             nondatetimes[i] = val
    
#     for key, value in datetimes.items():
#         print(f"{key} -> {value}")
#     for key, value in nondatetimes.items():
#         print(f"{key} -> {value}")