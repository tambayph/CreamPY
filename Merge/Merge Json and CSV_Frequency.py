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
with open('D:/Ezra/Python/Test/Data/Frequency.csv', encoding='ISO-8859-1') as f:
    reader = csv.reader(f)
    # Skip header row if it exists
    header = next(reader, None)
    # Loop over rows and add to JSON data
    for i, row in enumerate(reader):
        # Assuming the first column of the CSV contains ADM2_PCODE values
        adm3_group = row[0]
        # Assuming the second column of the CSV contains frequency values
        frequency = row[18]
        # Find the feature in the JSON data with the matching ADM2_PCODE
        for feature in data['features']:
            if feature['properties']['ADM3_GROUP'] == adm3_group:
                # Add the frequency value to the properties dictionary of the feature
                feature['properties']['Frequency'] = frequency
                break
        else:
            # If no matching feature was found, print a warning
            print(f'Warning: no feature found with ADM2_PCODE {adm3_group} (row {i+1})')

# save updated JSON file
with open('D:/Ezra/Python/Test/Municipal_Frequency.json', 'w') as f:
    json.dump(data, f)

