import pandas as pd
from datetime import datetime, timedelta
import re
from FuzzyDateParser import FuzzyDateParser



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