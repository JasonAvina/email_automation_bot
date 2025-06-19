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
        self.df['Parsed Return Date'] = self.df.apply(self.parse_row, axis = 1)
        
    # This function will do a few things:
    # - if row value is in datetime format, then value is returned
    # - else it will call parse(checkout_date, unparsed_return_date) method
    # This will convert the unparsed_return_date to a parsed_return_date in the proper format. 
    def parse_row(self, row):
        if pd.notna(row['Date Returned']):
            if isinstance(row['Date Returned'], datetime):
                return row['Date Returned']
            else:
                checkout_date = row['Date Checked Out']
                unparsed_return_date = row['Date Due']
                parsed_return_date = dateparser.parse(unparsed_return_date, settings={
                    'RELATIVE_BASE': checkout_date,
                    'PREFER_DATES_FROM': 'future'
            })
            return parsed_return_date
        else:
            return row['Date Returned']


            

