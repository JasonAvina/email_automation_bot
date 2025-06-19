#!/opt/anaconda3/bin/python3

import pandas as pd
from datetime import datetime, timedelta
import re
from data_load import load_checkout_data, inspect_rows, inspect_unique_values
from overdue_checker import print_overdue, check_for_overdue, print_overdue_rows
from FuzzyDateParser import FuzzyDateParser




# ------------------------------
# Main Logic
# ------------------------------
if __name__ == "__main__":

    FILE_PATH = "checkouts.xlsx"
    df = load_checkout_data(FILE_PATH)

    inspect = input('would you like to inspect the data before parsing?').lower().strip()
    if inspect == 'y':
        print(df.head())
        inspect_rows(df)
        #inspect_unique_values(df)
    parser = FuzzyDateParser(df)
    parser.add_parsed_column()
    #overdue_list = parser.get_overdue_rows()
    #parser.print_overdue(overdue_list)


    
    
    # print_overdue_rows(df)

