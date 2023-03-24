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
from datetime import datetime
from difflib import SequenceMatcher
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

df1 = pd.read_csv(
    r'D:\BI- Mark\CMPLBI_BV DataValidation\Copy\03-23-23\BV_CMPL_ETHICS_PHASES_VW.csv')  # reading sheet 1
df2 = pd.read_excel(
    r'D:\BI- Mark\CMPLBI_BV DataValidation\Copy\03-23-23\CMPL_ETHICS_PHASES_VW_UPD.xlsx')  # reading sheet 2
df3 = pd.read_excel(
    r'D:\BI- Mark\CMPLBI_BV DataValidation\Copy\03-23-23\Mapping File.xlsx')  # reading heading modeling file


# converting modeling file data to dictionary
def dataframe_to_dict(df, key_column, value_column):
    name_email_dict = df.set_index(key_column)[value_column].to_dict()
    return name_email_dict

df1[df1.columns[1]] = df1[df1.columns[1]].astype(str)
df1.sort_values(df1.columns[1], inplace=True)  # shorting values in sheet 1
df2[df2.columns[1]] = df2[df2.columns[1]].astype(str)
df2.sort_values(df2.columns[1], inplace=True)  # shorting values in sheet 2

def convert_to_date(date_string):
    """
    this function is converting improper date format to proper date format in order to compare the similarities.
    :param date_string:
    :return: date_object
    """
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

# Passing Columns with "Date" in the heading to be converted to the correct date format.
for i in df1.columns:
    j = str(i).lower()
    if j.__contains__('date'):
        df1[i] = list(map(convert_to_date, df1[i]))
        print('print for df1---------', df1[i])
for i in df2.columns:
    j = str(i).lower()
    if j.__contains__('date'):
        df2[i] = list(map(convert_to_date, df2[i]))
        print('print for df2---------', df2[i])

def col_data_comparison(col_data1, col_data2):
    """
    comparing two column data to check the similarity.
    :param col_data1: data from oracle description
    :param col_data2: data from snowflake description
    :return: True if data is similar, False if it is not similar
    """

    # print('inside function printing col1---', col_data1)
    # print('inside function printing col2---', col_data2)
    try:
        def clean_text(text):
            """
            this function is cleaning the data for any possible data dumps.
            :param text: data which needs to be cleaned
            :return: clean text
            """
            # Removing special characters
            noise_list = ['_x000D_']
            text = str(text) # this is newly added
            for k in noise_list:
                text = re.sub(k, '', text)
            # Remove non-alphanumeric characters and convert to lowercase
            text = re.sub(r'\W+', ' ', text).lower().strip()
            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text)
            # print('printing text---', text)
            return text

        try:
            cleaned_data1 = clean_text(col_data1)
        except:
            print('-------Except part col_data1--------', col_data1)
            print('-------Except part cleaned_data1--------', cleaned_data1)
        try:
            cleaned_data2 = clean_text(col_data2)
        except:
            print('-------Except part col_data2--------', col_data2)

        # Using SequenceMatcher
        seq_matcher = SequenceMatcher(None, cleaned_data1, cleaned_data2)
        ratio = seq_matcher.ratio()
        # print("SequenceMatcher Ratio:", ratio)

        # Using Cosine Similarity
        vectorizer = CountVectorizer().fit_transform([cleaned_data1, cleaned_data2])
        cos_sim = cosine_similarity(vectorizer)[0][1]
        # print("Cosine Similarity:", cos_sim)
        if ratio * 100 and cos_sim * 100 >= 90:
            # print('inside Try--- it is True')
            return True
        else:
            # print('inside Try--- it is False')
            return False
    except:
        if cleaned_data1 == cleaned_data2:
            # print('inside exception--- it is True')
            return True
        else:
            # print('inside exception--- it is False')
            return False

colName_dict = dataframe_to_dict(df3, 'Snowflake', 'Oracle') # here 'Snowflake' and 'Oracle' is the heading name in the
                                                            # mapping file. please change it according to the need.
df1 = df1.filter(colName_dict.values(), axis=1) # to filter the columns present in both dataset.
df2 = df2.filter(colName_dict.keys(), axis=1)
df2.rename(columns=colName_dict, inplace=True, )  # passing dictionary to make the heading same for both the sheets

columns_to_compare = df2.columns.values.tolist() # contains all the column name which we want to compare.
columns_to_compare.pop(0)

df1 = df1.drop_duplicates(subset=['ETHICS_CASE_NO'])

merged_df = df1.merge(df2, on='ETHICS_CASE_NO', how='outer', suffixes=('_Oracle', '_Snowflake')) # merging oracle
                                            # and snowflake data on the primary key value(here on='ETHICS_CASE_NUMBER').
merged_df['Data_Source'] = np.where(merged_df['ETHICS_CASE_NO'].isin(df1['ETHICS_CASE_NO']) &
                                    merged_df['ETHICS_CASE_NO'].isin(df2['ETHICS_CASE_NO']), 'Both',
                             np.where(merged_df['ETHICS_CASE_NO'].isin(df1['ETHICS_CASE_NO']), 'Oracle',
                             np.where(merged_df['ETHICS_CASE_NO'].isin(df2['ETHICS_CASE_NO']), 'Snowflake', np.nan)))


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
grouped_cols.append('ETHICS_CASE_NO')
for i in range(0, len(snowflake_grouped_cols)):
    grouped_cols.append(oracle_grouped_cols[i])
    grouped_cols.append(snowflake_grouped_cols[i])
grouped_cols.append('Data_Source')
differences = differences[grouped_cols]
# print(grouped_cols)
differences.drop_duplicates(inplace=True) # removing all the duplicat rows.
differences.dropna(subset=['ETHICS_CASE_NO'], inplace=True) # removing all the entries where Primary key is blank.

# removing leading and trailing whitespaces.
try:
    differences = differences.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
except:
    differences = differences.apply(lambda x: x.str.strip() if isinstance(x[0], str) else x)


def set_nan(row):
    '''
    removing data from both Oracle and Snowflake columns if both of them are same.(for related columns)
    :param row:
    :return: updated row
    '''
    for i in range(0, len(oracle_grouped_cols)):
        if row[oracle_grouped_cols[i]] == row[snowflake_grouped_cols[i]]:
            row[oracle_grouped_cols[i]] = np.nan
            row[snowflake_grouped_cols[i]] = np.nan
    return row
differences = differences.apply(lambda x: set_nan(x), axis=1)
differences.reset_index(drop=True, inplace=True) # Resetting the index after data cleaning.

# Replace #NUM! and #INF# errors with NaN
filtered_diff = differences.replace({'#NUM!': pd.np.nan, '#INF#': pd.np.inf, '-#INF#': -pd.np.inf, '#NaT#': pd.np.nan})

# Replace NaN values with blank cells
filtered_diff = filtered_diff.fillna('')

# ---Deep comparison for Case Description.
# filtered_diff['Similar'] = filtered_diff.apply(lambda row: col_data_comparison(row['DESCRIPTION_OF_RECOVERY_Oracle'], row['DESCRIPTION_OF_RECOVERY_Snowflake']), axis=1)
# filtered_diff.loc[filtered_diff['Similar'], ['DESCRIPTION_OF_RECOVERY_Oracle', 'DESCRIPTION_OF_RECOVERY_Snowflake']] = ''
# filtered_diff.drop('Similar', axis = 1, inplace = True)

# List of column names
columns = ['DESCRIPTION_OF_RECOVERY_Oracle', 'DESCRIPTION_OF_RECOVERY_Snowflake', 'column_name_3', 'column_name_4']

# Iterate through the list of column names
for i in range(0, len(oracle_grouped_cols)):
    # Apply the deep comparison function
    print(oracle_grouped_cols[i], '------------------', snowflake_grouped_cols[i])
    filtered_diff[f'Similar_{oracle_grouped_cols[i]}'] = filtered_diff.apply(lambda row: col_data_comparison(row[oracle_grouped_cols[i]], row[snowflake_grouped_cols[i]]), axis=1)
    # Replace the values in the original dataframe
    filtered_diff.loc[filtered_diff[f'Similar_{oracle_grouped_cols[i]}'], [oracle_grouped_cols[i], snowflake_grouped_cols[i]]] = ''
    # Drop the temporary column
    filtered_diff.drop(f'Similar_{oracle_grouped_cols[i]}', axis=1, inplace=True)


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
        try:
            worksheet.write(row_num + 1, col_num, value)
        except:
            # print(row_data.ETHICS_CASE_NO)
            continue
print('Workbook Closed.')
workbook.close()
