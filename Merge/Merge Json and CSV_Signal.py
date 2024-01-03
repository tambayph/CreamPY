# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 17:18:49 2023

@author: WF026
"""

import json
import csv

# Load the JSON data
with open('D:/Ezra/Python/Test/Data/Edited_Municipal.json') as f:
    data = json.load(f)

# Load the CSV data
with open('D:/Ezra/Python/Test/Signals/Dodong.csv', encoding='ISO-8859-1') as f:
    reader = csv.reader(f)
    # Skip header row if it exists
    header = next(reader, None)
    # Loop over rows and add to JSON data
    for i, row in enumerate(reader):
        # Assuming the first column of the CSV contains ADM2_PCODE values
        adm3_group = row[0]
        # Assuming the second column of the CSV contains frequency values
        Signals = row[3]
        # Find the feature in the JSON data with the matching ADM2_PCODE
        for feature in data['features']:
            if feature['properties']['ADM3_GROUP'] == adm3_group:
                # Add the frequency value to the properties dictionary of the feature
                feature['properties']['Signals'] = Signals
                
        else:
        # If no matching feature was found, set Signals to 0 
                feature['properties']['Signals'] = 0
                
# save updated JSON file
with open('D:/Ezra/Python/Test/Dodong.json', 'w') as f:
    json.dump(data, f)

