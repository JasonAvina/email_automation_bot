#!/opt/anaconda3/bin/python3

import pandas as pd
from datetime import datetime, timedelta
import re

# Load the Excel file
def load_checkout_data(file_path):
    """Load Excel file into a pandas DataFrame."""
    try:
        df = pd.read_excel(file_path)
        print("Excel file loaded successfully.")
        return df
    except Exception as e:
        print(f"Failed to load file: {e}")
        return None

# Parse fuzzy human-entered date strings
def parse_fuzzy_date(value):
    today = datetime.today().date()

    #if Expected Return Date entry is a string
    if isinstance(value, str):
        val = value.strip().lower()

        if val in ("eod", "end of day"):
            return today
        elif val in ("tomorrow", "tmrw"):
            return today + timedelta(days=1)
        elif val in ("end of week", "eow"):
            return today + timedelta(days=(4 - today.weekday()) % 7)  # Friday
        elif "monday" in val:
            return today + timedelta(days=(0 - today.weekday()) % 7)
        elif "friday" in val:
            return today + timedelta(days=(4 - today.weekday()) % 7)
        elif re.match(r"\d{1,2}/\d{1,2}/\d{2,4}", val):
            try:
                return pd.to_datetime(val, errors="coerce").date()
            except:
                return pd.NaT
        else:
            return pd.NaT
    #if Expected Return Date entry is a datetime
    elif isinstance(value, (datetime, pd.Timestamp)):
        return value.date()
    #if Expected Return Date is something else
    else:
        return pd.NaT

def add_parsed_return_dates(df):
    """Adds a 'Parsed Return Date' column to the DataFrame."""
    df['Parsed Return Date'] = df['Expected Return Date'].apply(parse_fuzzy_date)

# def add_send_reminder_flags(df):
#     """Adds a 'Send Reminder' column (True if overdue)."""
#     today = datetime.today().date()
#     df['Send Reminder'] = df['Parsed Return Date'].notna() & (df['Parsed Return Date'] < today)

# def get_rows_to_remind(df):
#     """Returns only the rows where Send Reminder is True."""
#     return df[df['Send Reminder'] == True]

# Main logic
if __name__ == "__main__":
    testing = True
    FILE_PATH = "LIB 80 Equipment Checkouts.xlsx"

    df = load_checkout_data(FILE_PATH)

    if df is not None:
        add_parsed_return_dates(df)
        # add_send_reminder_flags(df)
        # reminder_rows = get_rows_to_remind(df)

        # print("\n=== UNIQUE RETURN DATES ===")
        # uniquevals = sorted(df['Expected Return Date'].dropna().astype(str).unique())
        # for val in uniquevals:
        #     print(val)

        # if not reminder_rows.empty:
        #     print("\n=== PEOPLE TO REMIND ===")
        #     print(reminder_rows[['Name', 'Equipment Description', 'Expected Return Date', 'Parsed Return Date']])
        # else:
        #     print("No reminders needed.")
    while(testing):
        index = input("What row would you like to check?('0' to quit)")
        if index == '0':
            quit()
        else:
            index = int(index) - 1
            print(df.iloc[index])

