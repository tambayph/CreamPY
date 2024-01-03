# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 08:39:07 2023

@author: WF026
"""

import pandas as pd

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('D:/Ezra/Python/Test/output_mergeddata.csv', parse_dates=True)


# # Define input x and y values (replace with your own values)
x = input('Start Date (m/d/yyyy): ')
y = input('End Date (m/d/yyyy): ')


# Define input x and y values (replace with your own values)
# x = '1/21/2021'
# y = '1/23/2021'

# Get the input positions for the range of columns to be copied
x_pos = df.columns.get_loc(x)
y_pos = df.columns.get_loc(y)

# Select the first 4 columns and the range of columns to be copied based on their input positions
selected_cols = df.iloc[:, list(range(4)) + list(range(x_pos, y_pos+1))]

summ = selected_cols.loc[:,x:y]
summ = pd.to_numeric(summ.stack(), errors='coerce').unstack()

row_sums = summ.sum(axis=1)

selected_cols ['Accumulated'] = row_sums

selected_cols.to_csv('D:/Ezra/Python/Test/output_file.csv')
