import csv

import pandas as pd

df1 = pd.read_excel(
    r'OracleInput\D2.xlsx')  # reading sheet 1
df2 = pd.read_excel(
    r'SnowflakeInput\D1.xlsx')  # reading sheet 2
df3 = pd.read_excel(
    r'Column_Mapping_Data.xlsx')  # reading heading modeling file

def dataframe_to_dict(df, key_column, value_column):  # converting modeling file data to dictionary
    name_email_dict = df.set_index(key_column)[value_column].to_dict()
    return name_email_dict

df1.sort_values(df1.columns[1], inplace=True)  # shorting values in sheet 1
df2.sort_values(df2.columns[1], inplace=True)  # shorting values in sheet 2
df1.sort_index(axis=1)  # sorting the column name in ascending order
df2.sort_index(axis=1)  # sorting the column name in ascending order

# print(df1.columns)
# print(df2.columns)

colName_dict = dataframe_to_dict(df3, 'Snowflake', 'Oracle')
df2.rename(columns=colName_dict, inplace=True, )  # passing dictionary to make the heading same for both the sheets

l1 = df1.columns # have columns name from first sheet
l2 = df2.columns # have columns name from second sheet
l3 = [] # have column name which is there in both sheet one and two
str(l1).lower()
str(l2).lower()
for col in l1:
    if col in l2:
        l3.append(col)

df1 = df1.filter(l3, axis=1,) # to filter the columns present in both dataset.
df1.reset_index(drop=True, inplace=True)
df2 = df2.filter(l3, axis=1) # to filter the columns present in both dataset.
df2.reset_index(drop=True, inplace=True)

temp1 = []
temp2 = []
temp1.append(df1.columns)
temp2.append(df2.columns)
# print(temp1, '\n\n', temp2)

# pd.DataFrame(temp1).to_csv('Output\colNameList1.csv', index=0, header=0)
# pd.DataFrame(temp2).to_csv('Output\colNameList2.csv', index=0, header=0)
# pd.DataFrame(l3).to_csv('Output\colNameList3.csv', index=0, header=0)

# df4 = pd.concat([df1, df2]).drop_duplicates(keep=False)
# df4.to_csv(r'Output\final.csv')#, index=0)
# df_all = pd.concat([df1.set_index('ER_CASE_NUMBER'), df2.set_index('ER_CASE_NUMBER')],
#                    axis='columns', keys=['First', 'Second'])


merged = df1.merge(df2, how='outer', on=l3[0]) # df1- d2.xlsx | df2- d1.xlsx
cols = df1.columns
left = merged.iloc[:, :len(cols)].set_axis(cols, axis=1)
right = merged.iloc[:, len(cols):].set_axis(cols, axis=1) # ----issue
df4 = left.compare(right, keep_equal=False, keep_shape=True)
merged.to_csv(r'Output\trial.csv')
left.to_csv(r'Output\left.csv')
right.to_csv(r'Output\right.csv')


df4 = pd.concat([df1, df2]).loc[
    df1.index.symmetric_difference(df2.index)
]
print(df4)
df4.to_csv(r'Output\trial.csv')