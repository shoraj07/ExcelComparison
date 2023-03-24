from datetime import datetime
import pandas as pd

def convert_to_date(date_string):
    date_string = str(date_string)
    date_formats = ["%m-%d-%Y", "%m/%d/%Y", "%Y-%m-%d", "%Y/%m/%d"]
    for date_format in date_formats:
        try:
            # Extract just the date portion of the string by splitting on whitespace
            date_text = date_string.split()[0]
            date_object = datetime.strptime(date_text, date_format).date()
            return date_object
        except ValueError:
            return date_text
    return None # or return any other value you prefer to indicate an error

# example usage:
df1 = pd.read_csv(
    r'D:\BI- Mark\CMPLBI_BV DataValidation\Copy\03-23-23\BV_CMPL_ETHICS_PHASES_VW.csv')

date_object_4 = list(map(convert_to_date, df1['LAST_UPDATED_DATE']))

print(date_object_4)
