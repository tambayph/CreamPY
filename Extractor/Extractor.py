# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 12:53:29 2023

@author: WF026
"""

import pandas as pd

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('D:/Ezra/Python/Test/output.csv', parse_dates=True)
print(df.columns)

startdate = input('Start Date (m/d/yyyy) : ')
enddate = input('End Date (m/d/yyyy) : ')

# Get the input positions for the range of columns to be copied (replace 'x' and 'y' with the actual column positions, starting from 0)
x = df.columns.get_loc(startdate) # Convert the date string to the column position using get_loc() method
y = df.columns.get_loc(enddate) # Convert the date string to the column position using get_loc() method

# Select the first 3 columns and the range of columns to be copied based on their input positions
selected_cols = df.iloc[:, list(range(4)) + list(range(x, y+1))]

# Save the selected columns to a new CSV file, including the column names
selected_cols.to_csv('output_file.csv', index=False)


