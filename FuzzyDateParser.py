from datetime import datetime, timedelta
from dateutil import parser
import pandas as pd
import re

class FuzzyDateParser:
    def __init__(self, df, base_date=None):

        self.df = df
        self.base_date = base_date or datetime.today().date()

        # Common normalized mappings
        self.retval_conversion = {
            "today": self.base_date,
            "eod": self.base_date,
            "end of day": self.base_date,
            "end of the day": self.base_date,
            "tomorrow": self.base_date + timedelta(days=1),
            "next week": self.base_date + timedelta(weeks=1),
            "2 weeks": self.base_date + timedelta(weeks=2),
            "2 wks": self.base_date + timedelta(weeks=2),
            "an hour": self.base_date,  # conservative fallback
            "12:15 today": self.base_date,  # ignoring time portion
            "20th march": parser.parse("20 March").date(),  # parsed as a fixed calendar date
            "spring 2025": parser.parse("May 15 2025").date(),  # rough midpoint
            "summer 2025": parser.parse("July 15 2025").date(),  # rough midpoint
            "end of week": self.base_date + timedelta(days=(6 - self.base_date.weekday())),
            "end of the week": self.base_date + timedelta(days=(6 - self.base_date.weekday())),
            "end of semester": self._approx_semester_end(),
            "end of the semester": self._approx_semester_end(),
            "end of semenster": self._approx_semester_end(),
            "end of sementer": self._approx_semester_end(),
            "end of next semester": self._approx_semester_end(offset=1),
            "until end of spring sem": parser.parse("May 15").date(),
            "indefinite": None,
            "indefinetely": None,
            "indefinitely": None,
            "inddefinitely": None,
            "indefinietly": None,
            "indefinetly": None,
        }

    def _approx_semester_end(self, offset=0):
        # Default semester end: December 15 or May 15, depending on current date
        month = self.base_date.month
        year = self.base_date.year + offset
        if month <= 6:
            return datetime(year, 5, 15).date()  # Spring
        else:
            return datetime(year, 12, 15).date()  # Fall

    def parse_row(self, row):
        exp_ret_date = row['Expected Return Date']
        base_date = row['Date'] if isinstance(row['Date'], (datetime, pd.Timestamp)) else None
        return self.parse(exp_ret_date, base_date=base_date)
    
    def parse(self, date_str, base_date=None):
        if not date_str or not isinstance(date_str, str):
            return None

        base = base_date or self.base_date
        cleaned = date_str.lower().strip()

        # Try fixed mappings
        if cleaned in self.retval_conversion:
            return self.retval_conversion[cleaned]

        # Try partial match for common phrases
        for key in self.retval_conversion:
            if key in cleaned:
                return self.retval_conversion[key]

        # Regex fallback for "in X days/weeks"
        rel_match = re.match(r"in (\d+) (day|days|week|weeks)", cleaned)
        if rel_match:
            num = int(rel_match.group(1))
            unit = rel_match.group(2)
            days = num * 7 if "week" in unit else num
            return base + timedelta(days=days)

        # Fallback to dateutil.parser
        try:
            return parser.parse(cleaned, fuzzy=True).date()
        except Exception:
            return None
