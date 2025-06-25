
# Equipment Reminder Bot

This bot reads an Excel file of equipment checkouts and emails customers if their items are overdue.

# Structure

- Define the path to the Excel file
- Call load_checkout_data() to load the file
- If the file loads successfully:
    - Call add_parsed_return_dates() to parse fuzzy return dates
    - Call inspect_rows() to interactively view rows
- Store the data in the Parser Class for grouping together functions
- call OpenAI api to on batched rows to parse data with 1 api call
-check for overdue rows
-automate emails using microsoft outlook api

## Program Steps

✅ Load `.xlsx` file  
✅ Add 'Parsed Return Date' column to dataframe
🔜 Identify overdue items and make a list
🔜 Send emails to responsible customers on the list

## How to Run

1. Clone repo
2. Make sure the Excel file is in the same folder as main.py
3. Replace filepath in main.py with filepath of excel file
4. Run program

