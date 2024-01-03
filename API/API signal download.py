# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 08:12:21 2023

@author: WF026
"""

import requests
import csv

tcid = '1'
tcname = 'Amang'

url = f'http://10.10.1.97/fast/api/highest-signal/?id=2023{tcid}'

response = requests.get(url)

data = response.json()

# create a new CSV file for each id and write the headers
with open(f'D:/Ezra/Python/Test/Signals/{tcname}.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['geocode', 'province', 'municipality', 'signal'])

    # loop through the data and write each row to the CSV file
    for key in data['result']:
        row = [data['result'][key]['geocode'], data['result'][key]['province'], data['result'][key]['municipality'], data['result'][key]['signal']]
        writer.writerow(row)