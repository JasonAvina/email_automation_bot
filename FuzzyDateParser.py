from datetime import datetime, timedelta
import pandas as pd
import re
from openai import OpenAI
from typing import Dict, List, Optional


class FuzzyDateParser:
    def __init__(self, df, openai_api_key=None):
        self.df = df
        self.client = OpenAI(api_key=openai_api_key) if openai_api_key else OpenAI()

    def add_parsed_column(self):
        """Parse all dates with OpenAI in batch"""
        self.df.reset_index(drop=True, inplace=True)
        
        # Collect all unique unparsed dates that need parsing
        unique_dates = self._get_unique_dates_to_parse()
        
        # Get OpenAI to parse them all at once
        parsed_dates = self._batch_parse_with_openai(unique_dates)
        
        # Apply results to dataframe
        self._apply_results_to_dataframe(parsed_dates)

    def _get_unique_dates_to_parse(self):
        """Get unique date strings that need parsing (skip returned items)"""
        dates_to_parse = set()
        
        for _, row in self.df.iterrows():
            if pd.isna(row['Date Returned']):  # Only parse if not returned
                dates_to_parse.add(row['Date Due'])
        
        return list(dates_to_parse)

    def _batch_parse_with_openai(self, date_strings):
        """Send all dates to OpenAI in one call"""
        if not date_strings:
            return {}
            
        prompt = "Parse these due dates. Return each as YYYY-MM-DD or NONE if unparseable:\n"
        for i, date_str in enumerate(date_strings, 1):
            prompt += f"{i}. {date_str}\n"
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "system", 
                    "content": "You parse fuzzy dates. Return only YYYY-MM-DD format or NONE."
                }, {
                    "role": "user", 
                    "content": prompt
                }],
                temperature=0
            )
            
            return self._parse_response(response.choices[0].message.content, date_strings)
            
        except Exception as e:
            print(f"OpenAI error: {e}")
            return {date_str: None for date_str in date_strings}

    def _parse_response(self, response_text, date_strings):
        """Extract parsed dates from OpenAI response"""
        results = {}
        lines = response_text.strip().split('\n')
        
        for i, date_str in enumerate(date_strings):
            if i < len(lines):
                # Look for YYYY-MM-DD in the response line
                date_match = re.search(r'\d{4}-\d{2}-\d{2}', lines[i])
                if date_match:
                    try:
                        results[date_str] = datetime.strptime(date_match.group(), '%Y-%m-%d').date()
                    except ValueError:
                        results[date_str] = None
                else:
                    results[date_str] = None
            else:
                results[date_str] = None
        
        return results

    def _apply_results_to_dataframe(self, parsed_dates):
        """Apply parsed results to the dataframe"""
        def get_parsed_date(row):
            if pd.notna(row['Date Returned']):
                return row['Date Due']  # Don't parse if already returned
            
            return parsed_dates.get(row['Date Due'])
        
        self.df['Parsed Due Date'] = self.df.apply(get_parsed_date, axis=1)
        print(f"Made 1 OpenAI call to parse {len(parsed_dates)} unique dates for {len(self.df)} rows")

    
    def get_overdue_rows(self):
        """Return list of overdue items (not returned and past due date)"""
        today = datetime.now().date()
        overdue_rows = []
        
        for index, row in self.df.iterrows():
            # Skip if item already returned
            if pd.notna(row['Date Returned']):
                continue
                
            # Check if we have a parsed due date and it's in the past
            parsed_due_date = row['Parsed Due Date']
            if pd.notna(parsed_due_date) and parsed_due_date < today:
                overdue_rows.append({
                    'row_index': index,
                    'item': row.get('Item', 'Unknown'),
                    'borrower': row.get('Borrower', 'Unknown'), 
                    'due_date': parsed_due_date,
                    'days_overdue': (today - parsed_due_date).days
                })
        
        return overdue_rows