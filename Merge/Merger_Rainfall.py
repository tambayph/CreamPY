# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 08:03:28 2023

@author: WF026
"""


import pandas as pd


# Load the two Excel files into separate dataframes
file1 = pd.read_excel('D:/Ezra/Python/Test/template.xlsx')
file2 = pd.read_excel('D:/Ezra/Python/Test/rainfall.xlsx')

# Drop duplicates in each dataframe based on station number and date 
file2 = file2.drop_duplicates(subset=['StationNumber', 'Date'], keep='last')


# Merge the dataframes based on station number and date
merged_df = pd.merge(file1, file2, on='StationNumber', how='inner')
print(merged_df)

# Pivot the merged dataframe to display station number in rows and dates in columns
pivoted_df = merged_df.pivot(index=['StationNumber', 'Name', 'lat','lon'], columns='Date', values='Value')


print(pivoted_df)

# Export the pivoted dataframe to a new Excel file
pivoted_df.to_csv('D:/Ezra/Python/Test/output_merged.csv')



