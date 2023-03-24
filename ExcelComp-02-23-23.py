"""
----- change the file name and type as per the requirement. -----
- df1 = pd.read_excel(r'OracleInput\Oracle input file.xlsx')
- df2 = pd.read_csv(r'SnowflakeInput\Snowflake input file.csv')
- df3 = pd.read_excel(r'Mapping file.xlsx')
------------------------------------------------------------------------------------------------------------------------
----- Change the heading 1 and 2 value as per the Column mapping file. -----
- colName_dict = dataframe_to_dict(df3, 'heading 1', 'Heading 2')
------------------------------------------------------------------------------------------------------------------------
----- Change the primary key name as per the requirement. -----
- merged_df = df1.merge(df2, on='Primary key', how='outer', suffixes=('_Oracle', '_Snowflake'))
- grouped_cols.append('Primary Key')
- differences.dropna(subset=['Primary Key'], inplace=True)
"""


import pandas as pd
import numpy as np
import xlsxwriter

df1 = pd.read_excel(
    r'D:\BI- Mark\CMPLBI_BV DataValidation\Copy\D2.xlsx')  # reading sheet 1
df2 = pd.read_excel(
    r'D:\BI- Mark\CMPLBI_BV DataValidation\Copy\D1.xlsx')  # reading sheet 2
df3 = pd.read_excel(
    r'D:\BI- Mark\CMPLBI_BV DataValidation\Copy\col mapping-shoraj-12-05-22.xlsx')  # reading heading modeling file


def dataframe_to_dict(df, key_column, value_column):  # converting modeling file data to dictionary
    name_email_dict = df.set_index(key_column)[value_column].to_dict()
    return name_email_dict

df1.sort_values(df1.columns[1], inplace=True)  # shorting values in sheet 1
df2.sort_values(df2.columns[1], inplace=True)  # shorting values in sheet 2
df1.sort_index(axis=1)  # sorting the column name in ascending order
df2.sort_index(axis=1)  # sorting the column name in ascending order

colName_dict = dataframe_to_dict(df3, 'SFDC Column', 'Oracle Column') # here 'Snowflake' and 'Oracle' is the heading name in the
                                                            # mapping file. please change it according to the need.
df1 = df1.filter(colName_dict.values(), axis=1) # to filter the columns present in both dataset.
df2 = df2.filter(colName_dict.keys(), axis=1)
df2.rename(columns=colName_dict, inplace=True, )  # passing dictionary to make the heading same for both the sheets

columns_to_compare = df2.columns.values.tolist() # contains all the column name which we want to compare.
columns_to_compare.pop(0)

df1 = df1.drop_duplicates(subset=['ER_CASE_NUMBER'])

# merged_df = df1.merge(df2, on='ETHICS_CASE_NUMBER', how='outer', suffixes=('_Oracle', '_Snowflake')) # merging oracle
                                            # and snowflake data on the primary key value(here on='ETHICS_CASE_NUMBER').
merged_df = df1.merge(df2, on='ER_CASE_NUMBER', how='outer', suffixes=('_Oracle', '_Snowflake'))
merged_df['Data_Source'] = np.where(merged_df['ER_CASE_NUMBER'].isin(df1['ER_CASE_NUMBER']) & merged_df['ER_CASE_NUMBER'].isin(df2['ER_CASE_NUMBER']), 'Both',
                             np.where(merged_df['ER_CASE_NUMBER'].isin(df1['ER_CASE_NUMBER']), 'Oracle',
                             np.where(merged_df['ER_CASE_NUMBER'].isin(df2['ER_CASE_NUMBER']), 'Snowflake', np.nan)))


differences = pd.DataFrame()
for column in columns_to_compare:
    column_differences = merged_df[merged_df[column + '_Oracle'] != merged_df[column + '_Snowflake']]
    differences = differences.append(column_differences)


oracle_grouped_cols = [] # contains oracle headings
snowflake_grouped_cols = [] # contains Snowflake headings
grouped_cols = [] # contains all the column headings

'''Ordering Oracle and snowflake data one after another.'''
for i, col in enumerate(differences.columns):
    if "_Oracle" in col:
        oracle_grouped_cols.append(col)
    elif "_Snowflake" in col:
        snowflake_grouped_cols.append(col)
grouped_cols.append('ER_CASE_NUMBER')
for i in range(0, len(snowflake_grouped_cols)):
    grouped_cols.append(oracle_grouped_cols[i])
    grouped_cols.append(snowflake_grouped_cols[i])
grouped_cols.append('Data_Source')
differences = differences[grouped_cols]
print(grouped_cols)
differences.drop_duplicates(inplace=True) # removing all the duplicat rows.
differences.dropna(subset=['ER_CASE_NUMBER'], inplace=True) # removing all the entries where Primary key is blank.
# differences = differences.apply(lambda x: x.str.strip() if x.dtype == "object" else x) # removing leading and trailing whitespaces.
differences = differences.apply(lambda x: x.str.strip() if isinstance(x[0], str) else x) # removing leading and trailing whitespaces.


'''removing data from both Oracle and Snowflake columns if both of them are same.(for related columns)'''
def set_nan(row):
    for i in range(0, len(oracle_grouped_cols)):
        if row[oracle_grouped_cols[i]] == row[snowflake_grouped_cols[i]]:
            row[oracle_grouped_cols[i]] = np.nan
            row[snowflake_grouped_cols[i]] = np.nan
    return row
differences = differences.apply(lambda x: set_nan(x), axis=1)

# Replace #NUM! and #INF# errors with NaN
filtered_diff = differences.replace({'#NUM!': pd.np.nan, '#INF#': pd.np.inf, '-#INF#': -pd.np.inf})

# Replace NaN values with blank cells
filtered_diff = filtered_diff.fillna('')

# Create a workbook object with the 'nan_inf_to_errors' option set to True
workbook = xlsxwriter.Workbook(r'Output\output.xlsx', {'nan_inf_to_errors': True})

# Add a worksheet to the workbook
worksheet = workbook.add_worksheet()

# Define a format for the column headings
header_format = workbook.add_format({'bold': True, 'bg_color': 'yellow'})

# Write the column headings to the worksheet
for col_num, value in enumerate(filtered_diff.columns.values):
    if str(value).__contains__('_Oracle'):
        worksheet.write(0, col_num, value, header_format)
    else:
        worksheet.write(0, col_num, value)

# Write the data to the worksheet
for row_num, row_data in filtered_diff.iterrows():
    for col_num, value in enumerate(row_data):
        worksheet.write(row_num + 1, col_num, value)

# Close the workbook
workbook.close()
