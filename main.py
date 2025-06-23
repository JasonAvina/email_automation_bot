#!/opt/anaconda3/bin/python3

import pandas as pd
from data_load import load_checkout_data, inspect_rows, inspect_unique_values
from FuzzyDateParser import FuzzyDateParser
from Emails import Emails


# ------------------------------
# Main Logic
# ------------------------------
if __name__ == "__main__":

    FILE_PATH = "dummy_checkouts.xlsx"
    df = load_checkout_data(FILE_PATH)

    if df is not None:
        parser = FuzzyDateParser(df)
        parser.add_parsed_column()

        inspect = input('would you like to inspect the data now after parsing? ').lower().strip()
        if inspect == 'y':
            print(parser.df.head())
            inspect_rows(parser.df)
     
        # Get overdue items
        overdue_list = parser.get_overdue_rows()

        # Display overdue items
        print(f"\nFound {len(overdue_list)} overdue items:")
        if overdue_list:
            for item in overdue_list:
                print(f"- {item['item']} borrowed by {item['borrower']} (due {item['due_date']}, {item['days_overdue']} days overdue)")
        else:
            print("No overdue items found!")

        # Email automation (commented out for demo)
        if overdue_list:
            print(f"\n{'='*60}")
            print("EMAIL AUTOMATION PREVIEW")
            print(f"{'='*60}")
            
            # Uncomment these lines when ready to send actual emails:
            # email_handler = Emails(overdue_list)
            # email_handler.send_all_reminders()
            
            # For now, just show what emails would be sent
            email_handler = Emails(overdue_list)
            email_handler.send_all_reminders()  # This prints preview emails
            
            print(f"\n{'='*60}")
            print("To send actual emails:")
            print("1. Set EMAIL_PASSWORD environment variable")
            print("2. Uncomment the email sending lines above")
            print("3. Verify email addresses in your data")
            print(f"{'='*60}")
        else:
            print("\nNo overdue items, so no reminder emails needed.")
    
    else:
        print("Failed to load Excel file. Please check the file path and try again.")
  


