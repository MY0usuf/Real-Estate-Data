import pandas as pd
import pyarrow.parquet as pq
import numpy as np
from datetime import datetime

search_value = ['New','Al Barsha South Fourth','Unit','Residential','Dunes Tower','','',]
column_name = ['Version','Area','Property Type','Usage','Project','Property Size (sq.m)','Property Size (sq.ft)']

values = {'Ejari Contract Number':0,'Registration Date':0,'Start Date':0,'End Date':0,'Property ID':0,'Version':'None','Area':'None','Contract Amount':0,'Annual Amount':0,'Is Free Hold?':'None','Property Size (sq.m)':0,'Property Size (sq.ft)':0,'Amount (sq.m)':0,'Amount (sq.ft)':0,'Property Type':'None','Property Sub Type':'None','Number of Rooms':'None','Usage':'None','Parking':'None','No of Units':'None','Master Project':'None','Project':'None'}

dtypes = {'Ejari Contract Number':str,'Property ID':str,'Version':str,'Area':str,'Contract Amount':str,'Annual Amount':str,'Is Free Hold?':str,'Property Size (sq.m)':float,'Property Size (sq.ft)':float,'Amount (sq.m)':float,'Amount (sq.ft)':str,'Property Type':str,'Property Sub Type':str,'Number of Rooms':str,'Usage':str,'Parking':str,'No of Units':str,'Master Project':str,'Project':str}

table = pq.read_table('C:\\Users\\yousu\\Desktop\\python test\\main-flask\\raw_rental_data.parquet')
raw_data = table.to_pandas().reset_index()
raw_data['Start Date'] = pd.to_datetime(raw_data['Start Date'], format='%Y-%m-%d')

project_list = raw_data.Project.unique()
project_list = project_list.tolist()
project_list = sorted(project_list)
project_length = len(project_list)

area_list = raw_data.Area.unique()
area_list = area_list.tolist()
area_list = sorted(area_list)
area_length = len(area_list)

def search(search_value,column_name):
    # Initialising empty data frame
    matching_rows = pd.DataFrame()

    mask = pd.Series(np.ones(raw_data.shape[0], dtype=bool))

    for i in range(len(search_value)-1):
        if type(search_value[i]) == str:
            if len(search_value[i]) == 0:
                print(i)
                continue
            else:
                # Use the `&` operator to combine the boolean mask with the results of the current column search
                mask &= raw_data[column_name[i]] == search_value[i]
        elif i == 7:
            mask &= raw_data[(raw_data['Start Date'] >= search_value[7])]
        else:
            mask &= raw_data[column_name[i]] == search_value[i]
    matching_rows = raw_data[mask]
    matching_rows = matching_rows.loc[(matching_rows['Start Date'] >= search_value[7])]
    matching_rows.fillna(value = values, inplace=True)
    matching_rows.to_csv('C:\\Users\\yousu\\Desktop\\python test\\main-flask\\rental_results.csv', index=False)
    return matching_rows

def change(value):
    i = 0
    for i in range(len(value)):
        if i == 0:
            if value[i] == '0':
                value[i] = 'New'
            elif value[i] == '1':
                value[i] = 'Renewal'
            else:
                continue
        if i == 2:
            if value[i] == '1':
                value[i] = 'Land'
            elif value[i] == '2':
                value[i] = 'Building'
            elif value[i] == '3':
                value[i] = 'Unit'
            else:
                continue
        if i == 3:
            if value[i] == '1':
                value[i] = 'Residential'
            elif value[i] == '2':
                value[i] = 'Commercial'
            elif value[i] == '3':
                value[i] = 'Other'
            else:
                continue
        if i == 5:
            if len(value[i]) != 0:
                value[i] = float(value[i])
        if i == 6:
            if len(value[i]) != 0:
                value[i] = float(value[i])
        if i == 7:
            if value[i] != '':
                value[i] = datetime.strptime(value[i], '%Y-%m-%d')
            else:
                value[i] = datetime.strptime('2002-01-01', '%Y-%m-%d')
    return value