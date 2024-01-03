# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 13:57:49 2023

@author: WF026
"""

import os
import csv

# Set the directory path where CSV files are located
directory = 'D:/Ezra/Python/Test/csv/'

# Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        # Open the CSV file
        with open(directory + filename, 'r', encoding='iso-8859-1') as file:
            # Read the CSV data into a list
            data = list(csv.reader(file))

        # Replace 'ñ' with 'n' in each row of the data
        for row in data:
            for i, val in enumerate(row):
                row[i] = val.replace('ñ', 'n')

        # Write the updated data back to the CSV file
        with open(directory + filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(data)
