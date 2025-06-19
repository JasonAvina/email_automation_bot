from datetime import datetime, timedelta
from dateutil import parser
import dateparser
import pandas as pd
import re

class FuzzyDateParser:
    def __init__(self, df, base_date=None):
        self.df = df

    #this adds a column to the dataframe of 'expected return dates' that are in the datetime form
    def add_parsed_column(self):
        self.df['Parsed Due Date'] = self.df.apply(self.parse_row, axis = 1)
        
    # This function will do a few things:
    # - if row value is in datetime format, then value is returned
    # - else it will call parse(checkout_date, unparsed_return_date) method
    # This will convert the unparsed_return_date to a parsed_return_date in the proper format. 
    def parse_row(self, row):
        #if the item has been returned, return the due date
        if pd.notna(row['Date Returned']):
            return row['Date Due']
        #if return date is empty(item not returned) then parse the due date and return it
        else:
            checkout_date = datetime.strptime(row['Date Checked Out'], '%Y-%m-%d')
            unparsed_due_date = row['Date Due']
            parsed_due_date = dateparser.parse(unparsed_due_date, settings={
                'RELATIVE_BASE': checkout_date,
                'PREFER_DATES_FROM': 'future'
            })

            if parsed_due_date is None:
                print(f'check out date was {checkout_date} and unparsed due date was {unparsed_due_date}')
                try:
                    return pd.to_datetime(unparsed_due_date)
                except:
                    print("cant parse: ")
                    return parsed_due_date
                    
            return parsed_due_date


            

