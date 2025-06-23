from datetime import datetime, timedelta
from dateutil import parser
import dateparser
import pandas as pd
import re
import nltk


class FuzzyDateParser:
    def __init__(self, df, base_date=None):
        self.df = df

    #input: a class object that has a dataframe
    #action: calls a parse function on all rows on the Parsed Due Date Column
    def add_parsed_column(self):
        self.df['Parsed Due Date'] = self.df.apply(self.parse_row, axis = 1)
        
    #input: self and a Series(a single row from a dataframe)
    #action: iterates over each and parses a value in that row and returns it
    def parse_row(self, row):
        print(row.iloc[0])
        #if the item has been returned, return the due date
        if pd.notna(row['Date Returned']):
            print("returning original value")
            return row['Date Due']
        #if item has not been returned, parse it(if necessary) or just return the value(if in the proper format)
        else:
            #getting reference/base checkout date
            checkout_date = datetime.strptime(row['Date Checked Out'], '%Y-%m-%d')
            #trying to parse due date with traditional method
            parsed_due_date = dateparser.parse(row['Date Due'], settings={
                'RELATIVE_BASE': checkout_date,
                'PREFER_DATES_FROM': 'future'
            })
            #if parsing did not work, perform NLTK parsing
            if parsed_due_date is None:
                print("parsed due date is None type")
            else:
                print("parsed due date is Something")
                    
            return parsed_due_date


            

