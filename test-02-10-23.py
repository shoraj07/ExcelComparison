import pandas as pd
import numpy as np
from tabulate import tabulate

df1 = pd.read_excel(
    r'OracleInput\D2.xlsx')  # reading sheet 1
df2 = pd.read_excel(
    r'SnowflakeInput\D1.xlsx')  # reading sheet 2
# df3 = pd.read_excel(
#     r'CMPL BI_BV Tableau Dashboards_Mapping details.xlsx')  # reading heading modeling file

'''
def dataframe_to_dict(df, key_column, value_column):  # converting modeling file data to dictionary
    name_email_dict = df.set_index(key_column)[value_column].to_dict()
    return name_email_dict

df1.sort_values(df1.columns[1], inplace=True)  # shorting values in sheet 1
df2.sort_values(df2.columns[1], inplace=True)  # shorting values in sheet 2
df1.sort_index(axis=1)  # sorting the column name in ascending order
df2.sort_index(axis=1)  # sorting the column name in ascending order

# print(df1.columns)
# print(df2.columns)

colName_dict = dataframe_to_dict(df3, 'Snowflake View Name', 'CMPL_BI View Name')
df2.rename(columns=colName_dict, inplace=True, )  # passing dictionary to make the heading same for both the sheets

l1 = df1.columns # have columns name from first sheet
l2 = df2.columns # have columns name from second sheet
l3 = [] # have column name which is there in both sheet one and two
str(l1).lower()
str(l2).lower()
for col in l1:
    if col in l2:
        l3.append(col)

df1 = df1.filter(l3, axis=1) # to filter the columns present in both dataset.
df2 = df2.filter(l3, axis=1) # to filter the columns present in both dataset.

temp1 = []
temp2 = []
temp1.append(df1.columns)
temp2.append(df2.columns)
print(temp1, '\n\n', temp2)

# pd.DataFrame(temp1).to_csv('Output\colNameList1.csv', index=0, header=0)
# pd.DataFrame(temp2).to_csv('Output\colNameList2.csv', index=0, header=0)
# pd.DataFrame(l3).to_csv('Output\colNameList3.csv', index=0, header=0)

diff_matrix = df1.eq(df2)
diff_matrix = diff_matrix.applymap(lambda x: "" if x else "Different")

df1_result = df1.where(diff_matrix == "", other=diff_matrix)
df2_result = df2.where(diff_matrix == "", other=diff_matrix)

df1_result.to_excel('Output\df1_result.xlsx')
df2_result.to_excel('Output\df2_result.xlsx')
'''

'''
diff_rows = []
for i, row in df1.iterrows():
    diff_dict = {}
    case_number = row['ER_CASE_NUMBER']
    df2_row = df2[df2['ER_CASE_NUMBER'] == case_number]
    if df2_row.empty:
        continue
    else:
        df2_row = df2_row.iloc[0]
    for col in df1.columns:
        if row[col] != df2_row[col]:
            diff_dict['ER_CASE_NUMBER'] = case_number
            diff_dict[col] = row[col]
    diff_rows.append(diff_dict)

result = pd.DataFrame(diff_rows)
print(tabulate(result, showindex=False, headers=df1.columns))
result.to_excel(r'Output\result.xlsx')
'''

merged_df = df1.merge(df2, on='ER_CASE_NUMBER', how='outer', suffixes=('_df1', '_df2'))
differences = merged_df[merged_df['SENSITIVE_FLAG_df1'] != merged_df['SENSITIVE_FLAG_df2']]
differences = differences.append(merged_df[merged_df['ER_CASE_QUEUE_df1'] != merged_df['ER_CASE_QUEUE_df2']])
differences = differences.append(merged_df[merged_df['ER_CASE_OWNER_df1'] != merged_df['ER_CASE_OWNER_df2']])
differences = differences.append(merged_df[merged_df['ER_CASE_STATUS_df1'] != merged_df['ER_CASE_STATUS_df2']])
differences = differences.append(merged_df[merged_df['ER_CASE_SUBJECT_df1'] != merged_df['ER_CASE_SUBJECT_df2']])
differences = differences.append(merged_df[merged_df['ER_DIVISION_df1'] != merged_df['ER_DIVISION_df2']])
differences = differences.drop_duplicates(subset=['ER_CASE_NUMBER'])
differences = differences.set_index('ER_CASE_NUMBER')
# filtered_differences = differences.loc[:, (differences != differences.iloc[0]).any()]

differences.to_excel(r'Output\differences.xlsx')
# filtered_differences.to_excel(r'Output\filtered_differences.xlsx')


# merged_df = pd.merge(df1, df2, on='ER_CASE_NUMBER', how='outer', indicator=True)
# uncommon_df = merged_df[merged_df['_merge'] != 'both']

# uncommon_df.to_excel(r'Output\uncommon_df.xlsx')


# merged_df = pd.merge(df1, df2, on='ER_CASE_NUMBER', how='inner', indicator=True)
# common_df = merged_df[merged_df['_merge'] == 'both']
#
# df1 = df1[df1['ER_CASE_NUMBER'].isin(common_df['ER_CASE_NUMBER'])]
# df2 = df2[df2['ER_CASE_NUMBER'].isin(common_df['ER_CASE_NUMBER'])]
