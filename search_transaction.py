import pandas as pd
import pyarrow.parquet as pq
import numpy as np
from datetime import datetime

search_value = ['', '', 'Capital Bay  A', 'Business Bay', 'Residential', 'Unit', '', '']
column_name = ['Transaction Type', 'Registration type', 'Project', 'Area', 'Usage', 'Property Type', 'Property Size (sq.ft)', 'Property Size (sq.m)']

# Read the CSV file into a DataFrame

table = pq.read_table('C:\\Users\\yousu\\Desktop\\python test\\main-flask\\raw_transaction_data.parquet')
matches = table.to_pandas().reset_index()
matches['Transaction Date'] = pd.to_datetime(matches['Transaction Date'], format='%Y-%m-%d')
values = {'Transaction Number':0,'Transaction Date':0,'Property ID':0,'Transaction Type':'None','Transaction sub type':'None','Registration type':'None','Is Free Hold?':'None','Usage':'None','Area':'None','Property Type':'None','Property Sub Type':'None','Amount':0.0,'Transaction Size (sq.m)':0,'Property Size (sq.m)':0,'Property Size (sq.ft)':0,'Amount (sq.m)':0,'Amount (sq.ft)':0,'Room(s)':'None','Parking':'None','No. of Buyer':0,'No. of Seller':0,'Master Project':'None','Project':'None'}

matches.fillna(value = values, inplace=True)

project_list = matches.Project.unique()
project_list = project_list.tolist()
project_list = sorted(project_list)
project_length = len(project_list)

area_list = matches.Area.unique()
area_list = area_list.tolist()
area_list = sorted(area_list)
area_length = len(area_list)

property_sub_type_list = matches['Property Sub Type'].unique()
property_sub_type_list = property_sub_type_list.tolist()
property_sub_type_list = sorted(property_sub_type_list)
property_sub_type_length = len(property_sub_type_list)

def search(search_value, column_name):
    # Initialize an empty DataFrame to store the matching rows
    matching_rows = pd.DataFrame()

    mask = pd.Series(np.ones(matches.shape[0], dtype=bool))

    for i in range(len(search_value)-1):
        if type(search_value[i]) == str:
            if len(search_value[i]) == 0:
                print(i)
                continue
            else:
                # Use the `&` operator to combine the boolean mask with the results of the current column search
                mask &= matches[column_name[i]] == search_value[i]
        elif i == 9:
            mask &= matches[(matches['Transaction Date'] > search_value[9])]
        else:
            mask &= matches[column_name[i]] == search_value[i]
        
    matching_rows = matches[mask]
    matching_rows = matching_rows.loc[(matching_rows['Transaction Date'] >= search_value[9])]
    matching_rows.fillna(value = 0, inplace=True)
    matching_rows.style.format("{:.2f}")
    matching_rows.to_csv('C:\\Users\\yousu\\Desktop\\python test\\main-flask\\transaction_results.csv', index=False)
    return matching_rows
'''    print(matching_rows)
    matching_rows.to_csv('results.csv', index=False)'''

def change(value):
    i = 0
    for i in range(10):
        if i == 0:
            if value[i] == '1':
                value[i] = 'Sales'
            elif value[i] == '2':
                value[i] = 'Mortgages'
            elif value[i] == '3':
                value[i] = 'Gifts'
            else:
                continue
        if i == 1:
            if value[i] == '0':
                value[i] = 'Ready'
            elif value[i] == '1':
                value[i] = 'Off-Plan'
            else:
                continue
        if i == 4:
            if value[i] == '1':
                value[i] = 'Residential'
            elif value[i] == '2':
                value[i] = 'Commercial'
            elif value[i] == '3':
                value[i] = 'Other'
            else:
                continue
        if i == 5:
            if value[i] == '1':
                value[i] = 'Land'
            elif value[i] == '2':
                value[i] = 'Building'
            elif value[i] == '3':
                value[i] = 'Unit'
            else:
                continue
        if i == 7:
            if len(value[i]) != 0:
                value[i] = float(value[i])
        if i == 8:
            if len(value[i]) != 0:
                value[i] = float(value[i])
        if i == 9:
            if value[i] != '':
                value[i] = datetime.strptime(value[i], '%Y-%m-%d')
            else:
                value[i] = datetime.strptime('2002-01-01', '%Y-%m-%d')


    return value
            