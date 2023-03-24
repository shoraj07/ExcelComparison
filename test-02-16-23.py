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

df1 = pd.read_excel(
    r'OracleInput\ETHICS_CASES_LATEST_VW.xlsx')  # reading sheet 1
df2 = pd.read_csv(
    r'SnowflakeInput\BV_SFDC_ETHICS_CASES_LATEST.csv')  # reading sheet 2
df3 = pd.read_excel(
    r'Mapping_Data.xlsx')  # reading heading modeling file


def dataframe_to_dict(df, key_column, value_column):  # converting modeling file data to dictionary
    name_email_dict = df.set_index(key_column)[value_column].to_dict()
    return name_email_dict

df1.sort_values(df1.columns[1], inplace=True)  # shorting values in sheet 1
df2.sort_values(df2.columns[1], inplace=True)  # shorting values in sheet 2
df1.sort_index(axis=1)  # sorting the column name in ascending order
df2.sort_index(axis=1)  # sorting the column name in ascending order

colName_dict = dataframe_to_dict(df3, 'Snowflake', 'Oracle') # here 'Snowflake' and 'Oracle' is the heading name in the
                                                            # mapping file. please change it according to the need.
df1 = df1.filter(colName_dict.values(), axis=1) # to filter the columns present in both dataset.
df2 = df2.filter(colName_dict.keys(), axis=1)
df2.rename(columns=colName_dict, inplace=True, )  # passing dictionary to make the heading same for both the sheets

columns_to_compare = df2.columns.values.tolist() # contains all the column name which we want to compare.
columns_to_compare.pop(0)

# merged_df = df1.merge(df2, on='ETHICS_CASE_NUMBER', how='outer', suffixes=('_Oracle', '_Snowflake')) # merging oracle
                                            # and snowflake data on the primary key value(here on='ETHICS_CASE_NUMBER').
merged_df = df1.merge(df2, on='ETHICS_CASE_NUMBER', how='outer', suffixes=('_Oracle', '_Snowflake'))
merged_df['Data_Source'] = np.where(merged_df['ETHICS_CASE_NUMBER'].isin(df1['ETHICS_CASE_NUMBER']) & merged_df['ETHICS_CASE_NUMBER'].isin(df2['ETHICS_CASE_NUMBER']), 'Both',
                             np.where(merged_df['ETHICS_CASE_NUMBER'].isin(df1['ETHICS_CASE_NUMBER']), 'Oracle',
                             np.where(merged_df['ETHICS_CASE_NUMBER'].isin(df2['ETHICS_CASE_NUMBER']), 'Snowflake', np.nan)))


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
grouped_cols.append('ETHICS_CASE_NUMBER')
for i in range(0, len(snowflake_grouped_cols)):
    grouped_cols.append(oracle_grouped_cols[i])
    grouped_cols.append(snowflake_grouped_cols[i])
grouped_cols.append('Data_Source')
differences = differences[grouped_cols]
print(grouped_cols)
differences.drop_duplicates(inplace=True) # removing all the duplicat rows.
differences.dropna(subset=['ETHICS_CASE_NUMBER'], inplace=True) # removing all the entries where Primary key is blank.
differences = differences.apply(lambda x: x.str.strip() if x.dtype == "object" else x) # removing leading and trailing whitespaces.

'''removing data from both Oracle and Snowflake columns if both of them are same.(for related columns)'''
def set_nan(row):
    for i in range(0, len(oracle_grouped_cols)):
        if row[oracle_grouped_cols[i]] == row[snowflake_grouped_cols[i]]:
            row[oracle_grouped_cols[i]] = np.nan
            row[snowflake_grouped_cols[i]] = np.nan
    return row
differences = differences.apply(lambda x: set_nan(x), axis=1)

filtered_Both = merged_df[merged_df['Data_Source'] == 'Both']
filtered_Oracle = merged_df[merged_df['Data_Source'] == 'Oracle']
filtered_Snowflake = merged_df[merged_df['Data_Source'] == 'Snowflake']

filtered_diff = differences.style.set_table_styles([{'selector': 'th', 'props': [('background-color', 'yellow')]
                                    if col in oracle_grouped_cols else []} for col in differences.columns])
filtered_diff.to_excel(r'Output\filtered_diff-Oracle-SFDC_Comp.xlsx',index= False, sheet_name= 'Oracle-SFDC')

writer = pd.ExcelWriter(r'Output\Oracle-SFDC_Comp.xlsx', engine='xlsxwriter')
filtered_Both.to_excel(writer, sheet_name='Oracle-SFDC_Comp')
filtered_Oracle.to_excel(writer, sheet_name='Oracle')
filtered_Snowflake.to_excel(writer, sheet_name='Snowflake')
writer.save()