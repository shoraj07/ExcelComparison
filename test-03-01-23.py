import pandas as pd
import xlsxwriter

# Create a sample dataframe with NaN and INF values
filtered_diff = pd.read_excel(r'Output\filtered_diff-Oracle-SFDC_Comp.xlsx')

# Replace #NUM! and #INF# errors with NaN
filtered_diff = filtered_diff.replace({'#NUM!': pd.np.nan, '#INF#': pd.np.inf, '-#INF#': -pd.np.inf})

# Replace NaN values with blank cells
filtered_diff = filtered_diff.fillna('')

# Create a workbook object with the 'nan_inf_to_errors' option set to True
workbook = xlsxwriter.Workbook('output.xlsx', {'nan_inf_to_errors': True})

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



# filtered_Both = merged_df[merged_df['Data_Source'] == 'Both']
# filtered_Oracle = merged_df[merged_df['Data_Source'] == 'Oracle']
# filtered_Snowflake = merged_df[merged_df['Data_Source'] == 'Snowflake']
#
# filtered_diff = differences.style.set_table_styles([{'selector': 'th', 'props': [('background-color', 'yellow')]
#                                     if col in oracle_grouped_cols else []} for col in differences.columns])
# filtered_diff.to_excel(r'Output\filtered_diff-Oracle-SFDC_Comp.xlsx',index= False, sheet_name= 'Oracle-SFDC')
# df2.to_excel(r'Output\D1---.xlsx',index= False)
# df1.to_excel(r'Output\D2---.xlsx',index= False)
