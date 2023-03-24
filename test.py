# import pandas as pd
#
# df1 = pd.read_excel(r'D:\BI- Mark\automation Sample data\Copy\Test\t1.xlsx')
# df2 = pd.read_excel(r'D:\BI- Mark\automation Sample data\Copy\Test\t2.xlsx')
# df3 = pd.read_excel(r'D:\BI- Mark\automation Sample data\Copy\col mapping-shoraj-12-05-22.xlsx')
#
#
# def dataframe_to_dict(df, key_column, value_column):
#     name_email_dict = df.set_index(key_column)[value_column].to_dict()
#     return name_email_dict
#
#
# df1.sort_values('TC_Case_Number__c', inplace=True)
# df2.sort_values('ER_CASE_NUMBER', inplace=True)
#
# colName_dict = dataframe_to_dict(df3, 'Oracle Column', 'SFDC Column')
#
# df2.rename(columns=colName_dict, inplace=True)
#
# diff_df = pd.concat([df1, df2]).loc[
#     df1.index.symmetric_difference(df2.index)
# ]
# diff_df.to_excel('diff.xlsx')
# print(diff_df)

import pandas as pd

# create a sample dataframe
data = {'Name': ['John', 'Mary', 'Peter'], 'Age': [25, 30, 35], 'City': ['New York', 'London', 'Paris']}
df = pd.DataFrame(data)

# create a list of heading names
heading_list = list(df.columns)

# create a styler object and apply a background color to the heading cells
styler = df.style.set_table_styles([{'selector': 'th', 'props': [('background-color', 'yellow')] if col in heading_list else []} for col in df.columns])

# display the styled dataframe
styler.to_excel()
