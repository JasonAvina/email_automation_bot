# Equipment Reminder Bot

This bot reads an Excel file of equipment checkouts and emails professors if their items are overdue.

# Structure

- Define the path to the Excel file
- Call load_checkout_data() to load the file
- If the file loads successfully:
    - Call add_parsed_return_dates() to parse fuzzy return dates
    - Call inspect_rows() to interactively view rows
- Store the data in the Parser Class for grouping together functions
- call 


## Program Steps

✅ Load `.xlsx` file  
✅ Add 'Parsed Return Date' column to dataframe
🔜 Identify overdue items and make a list
🔜 Send emails to responsible professors on the list

## How to Run

1. Open the terminal or double-click `equipment_bot.pyw`
2. Make sure the Excel file is in the same folder (or adjust `FILE_PATH`)
3. Check output in the terminal or logs

## To Do

- [ ] Fix Excel path if using Box Drive
- [ ] Add logging of sent emails
- [ ] Group multiple items per professor into one email
- [ ] Format and test email sending
