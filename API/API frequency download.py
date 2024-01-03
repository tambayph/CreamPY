# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 11:42:46 2023

@author: WF026
"""

import requests
import csv

# # loop through ids from 20211 to 20215
# for id in range(1, 16):
#     url = f'http://10.10.1.97/fast/api/frequent-signal/?id=2021{id}'

#     response = requests.get(url)

#     data = response.json()
#     print(data)

#     # create a new CSV file for each id and write the headers
#     with open(f'Frequency_{id}.csv', mode='w', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(['geocode', 'province', 'municipality', 'frequency'])

#         # loop through the data and write each row to the CSV file
#         for key in data['result']:
#             row = [data['result'][key]['geocode'], data['result'][key]['province'], data['result'][key]['municipality'], data['result'][key]['frequency']]
#             writer.writerow(row)

# loop through ids from 20211 to 20215

url = 'http://10.10.1.97/fast/api/frequent-signal/?id=20234'

response = requests.get(url)

data = response.json()
print(data)

# create a new CSV file for each id and write the headers
with open('Frequency.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['geocode', 'province', 'municipality', 'frequency'])

    # loop through the data and write each row to the CSV file
    for key in data['result']:
        row = [data['result'][key]['geocode'], data['result'][key]['province'], data['result'][key]['municipality'], data['result'][key]['frequency']]
        writer.writerow(row)