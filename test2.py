# columns = ['ER_CASE_NUMBER', 'SENSITIVE_FLAG_df1', 'ER_CASE_QUEUE_df1', 'ER_CASE_OWNER_df1', 'ER_CASE_STATUS_df1',
#            'ER_CASE_SUBJECT_df1', 'ER_DIVISION_df1', 'SENSITIVE_FLAG_df2', 'ER_CASE_QUEUE_df2', 'ER_CASE_OWNER_df2',
#            'ER_CASE_STATUS_df2', 'ER_CASE_SUBJECT_df2', 'ER_DIVISION_df2']
#
# grouped_cols = []
# for i, col in enumerate(columns):
#     if "_df1" in col:
#         grouped_cols.append(col)
#     elif "_df2" in col:
#         grouped_cols.append(col)
#
# print(grouped_cols)
#
#
# # ----------------------------------------------------------------------------------------------------------------------
# merged_df = df1.merge(df2, on='ETHICS_CASE_NUMBER', how='outer', suffixes=('_df1', '_df2'))
#
# columns_to_compare = ['MAIN_ASSIGNEE', 'MODIFIED_ON', 'MODIFIED_BY', 'BRIEF_CASE_DESCRIPTION','CURRENT_PHASE',
#                       'ETHICS_CASE_TYPE', 'IS_ANNONYMOUS', 'INQUIRY_TYPE', 'COMPLIANCE_RISK_AREA', 'INTAKE_SOURCE',
#                       'INTAKE_CREATED_DATE', 'INTAKE_REFERENCE_NUMBER', 'CASE_SUBMITTER_NAME',
#                       'IS_VALID_CISCO_EMPLOYEE', 'INCIDENT_LOC_CITY', 'INCIDENT_START_DATE',
#                       'INCIDENT_LOCATION_COUNTRY', 'INCIDENT_END_DATE', 'INCIDENT_LOCATION_THEATER',
#                       'IS_MANAGER_AWARE_OF', 'CAN_WE_CONTACT_YOUR_MANAGER', 'LAST_UPDATED_ON', 'PHASE_TRANSITIONED_ON',
#                       'FINAL_DISPOSITION', 'ACTION_TAKEN', 'RECOMMENDED_TRAINING', 'RECOMMENDED_REGULATION_OR_LAW',
#                       'FISCAL_YEAR', 'FISCAL_QUARTER', 'SEQ']
#
# differences = pd.DataFrame()
# for column in columns_to_compare:
#     column_differences = merged_df[merged_df[column + '_df1'] != merged_df[column + '_df2']]
#     differences = differences.append(column_differences)
#
# print(differences)

import pandas as pd
from tabulate import tabulate
import numpy as np

df1 = pd.DataFrame({'ETHICS_CASE_NUMBER': ['ETHICS-111022-6632', 'ETHICS-102622-6528', 'ETHICS-110822-6610'],
                   'MAIN_ASSIGNEE_Oracle': ['Ethics Office,   ', 'Ethics Office,    ', 'Ethics Office,'],
                   'MAIN_ASSIGNEE_Snowflake': ['Ethics Office,', 'Ethics Office,', 'Global Procurement Services'],
                   'MODIFIED_ON_Oracle': ['2022-11-10 13:43:58', '2022-10-27 17:40:36', '2022-11-09 08:47:32'],
                   'MODIFIED_ON_Snowflake': ['2022-11-10 13:43:58', '2022-10-27 00:00:00.000 -0700', '2022-11-09 00:00:00.000 -0800']})
l1 = ['MAIN_ASSIGNEE_Oracle', 'MODIFIED_ON_Oracle']
l2 = ['MAIN_ASSIGNEE_Snowflake', 'MODIFIED_ON_Snowflake']
df1 = df1.apply(lambda x: x.str.strip())
def set_nan(row):
    for i in range(0, len(l1)):
        if row[l1[i]] == row[l2[i]]:
            row[l1[i]] = np.nan
            row[l2[i]] = np.nan
    return row

df1 = df1.apply(lambda x: set_nan(x), axis=1)
print(tabulate(df1, headers=df1))