# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 08:38:06 2023

@author: WF026
"""

import pandas as pd


# Load the two Excel files into separate dataframes
file1 = pd.read_csv('D:/Ezra/Python/Scripts/Merged_Frequency.csv')

file2 = pd.read_csv('D:/Ezra/Python/Scripts/Frequency_15.csv')

# merge the two dataframes on the columns 'geocode', 'province', and 'municipality'
merged_df = pd.merge(file1, file2, on=['geocode', 'province', 'municipality'] , how='outer')

# write the merged dataframe to a new CSV file
merged_df.to_csv('D:/Ezra/Python/Scripts/Merged_Frequency.csv', index=False)
