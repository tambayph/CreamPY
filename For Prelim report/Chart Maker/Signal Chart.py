# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 11:36:41 2023

@author: WF026
"""

import requests
import csv
import json
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

####### Only change this part #######


with open("input.txt", "r") as file:
    lines = file.readlines()
    selected_file_path = lines[0].strip()
    selected_file_dir = lines[1].strip()

# Input the filename
tcid = selected_file_path
tcname = selected_file_dir
fastid = int(selected_file_path)
####### Only change this part #######

###################################################

gdfdir = f'D:/Ezra/Python/Test/Signals/JSON/{tcname}.json'
sdfdir = 'Edited_Province.json'
dfdir = f'D:/Ezra/Python/Test/Tracks/2023/PH2023{tcid}.txt'
savedir = 'D:/Ezra/Python/Test/'+tcname

############### Download API #####################
url = f'http://10.10.1.97/fast/api/highest-signal/?id=2023{fastid}'

response = requests.get(url)

data = response.json()

# create a new CSV file for each id and write the headers
with open(f'D:/Ezra/Python/Test/Signals/CSV/{tcname}.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['geocode', 'province', 'municipality', 'signal'])

    # loop through the data and write each row to the CSV file
    for key in data['result']:
        row = [data['result'][key]['geocode'], data['result'][key]['province'], data['result'][key]['municipality'], data['result'][key]['signal']]
        writer.writerow(row)
        
############### Merge JSON #####################

# Load the JSON data
with open('Edited_Municipal.json') as f:
    data = json.load(f)

# Load the CSV data
with open(f'D:/Ezra/Python/Test/Signals/CSV/{tcname}.csv', encoding='ISO-8859-1') as f:
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
with open(f'D:/Ezra/Python/Test/Signals/JSON/{tcname}.json', 'w') as f:
    json.dump(data, f)

############### Create Chart #####################

# Read in the GeoJSON file
gdf = gpd.read_file(gdfdir)
sdf = gpd.read_file(sdfdir)

# Define the frequency values and corresponding colors
color_dict = {'1': '#00CCFF', '2': '#FFFF00', '3': '#FFC000', '4': '#FF0000', '5': '#FF00FF'}

# Define a function to return the color for each value
def get_color(value):
    return color_dict.get(str(value), '#73b273')

# Plot the GeoDataFrame with custom colors
fig, ax = plt.subplots(figsize=(17, 22), dpi=450)
gdf.plot(ax=ax, column='Signals', color=[get_color(value) for value in gdf['Signals']])

# Remove the numbers on the axis
ax.set_xticks([])
ax.set_yticks([])

# Set the face color and edge color
ax.set_facecolor('#002673')
# Set the edge color for all sides
for spine in ax.spines.values():
    spine.set_color('white')


# Create legend handles and labels
handles = [mpatches.Patch(color=color_dict[str(i)], label='TCWS #' + ' ' + str(i)) for i in range(5, 0, -1)]
labels = [h.get_label() for h in handles]

# Add legend to the plot
ax.legend(handles=handles, labels=labels, loc='upper left',  prop={'family': 'Arial', 'weight': 'bold', 'size': 18})

# Show the plot)

# Set the background color of the legend frame to black
ax.get_legend().get_frame().set_facecolor('black')

ax.get_legend().get_title().set_color('white')

# Set the font color of the legend labels to white
for text in ax.get_legend().get_texts():
    text.set_color("white")

# Add sdf as a transparent overlay
sdf.plot(ax=ax, facecolor='none', edgecolor='black', alpha=1)

###############################################################################
#PUT TRACK
############################################################################### 
# Read the data from the text file
df = pd.read_csv(dfdir, sep='\s+', names=['col1', 'lat', 'lon', 'col4', 'col5', 'col6'], skiprows=1)

# Convert the coordinates to decimal degrees format
df['lat'] = df['lat'] / 10.0
df['lon'] = df['lon'] / 10.0
df['lat'] = df['lat'].round(1)
df['lon'] = df['lon'].round(1)

# Create a new column with the combined coordinates
df['coords'] = list(zip(df['lat'], df['lon']))
###############################################################################
#SET BOUNDARIES
###############################################################################    
# Open the JSON file
with open(gdfdir) as f:
    # Load the JSON data
    data = json.load(f)

signal_values = [1, 2, 3, 4, 5]  # The desired signal values

filtered_features = []

for feature in data['features']:
    signal = feature['properties'].get('Signals')
    if signal is not None and int(signal) in signal_values:
        filtered_features.append(feature)

lowest_lat = float('inf')
lowest_lon = float('inf')
highest_lat = float('-inf')
highest_lon = float('-inf')

def process_coordinates(coordinates):
    global lowest_lat, lowest_lon, highest_lat, highest_lon
    
    if isinstance(coordinates[0], list):
        for coord in coordinates:
            process_coordinates(coord)
    else:
        lat = coordinates[1]
        lon = coordinates[0]
        
        if lat < lowest_lat:
            lowest_lat = lat
            
        if lon < lowest_lon:
            lowest_lon = lon
        
        if lat > highest_lat:
            highest_lat = lat
            
        if lon > highest_lon:
            highest_lon = lon

for feature in filtered_features:
    coordinates = feature['geometry']['coordinates']
    process_coordinates(coordinates)

ymin = lowest_lat - 0.5
xmin = lowest_lon - 0.5
ymax = highest_lat + 0.5
xmax = highest_lon + 0.5 

# Desired aspect ratio
new_width = 17
new_height = 22
aspect_ratio = new_width / new_height

# Calculate the center of the original rectangle
xcenter = (xmin + xmax) / 2
ycenter = (ymin + ymax) / 2

# Calculate the width and height of the original rectangle
width = xmax - xmin
height = ymax - ymin

# Calculate the aspect ratio of the original rectangle
original_aspect_ratio = width / height

if original_aspect_ratio > aspect_ratio:
    # The rectangle is wider than the desired aspect ratio
    # Adjust the height to match the aspect ratio
    new_height = width / aspect_ratio
    # Shift the rectangle to the center
    ymin = ycenter - new_height / 2
    ymax = ycenter + new_height / 2
else:
    # The rectangle is taller than the desired aspect ratio
    # Adjust the width to match the aspect ratio
    new_width = height * aspect_ratio
    # Shift the rectangle to the center
    xmin = xcenter - new_width / 2
    xmax = xcenter + new_width / 2

# # set the new limits for the plot
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)

# Overlay the line from the text file on top of the plot
ax.plot(df['lon'], df['lat'], color='white', lw=4)

# Create the directory if it doesn't exist
if not os.path.exists(savedir):
    os.makedirs(savedir)

savedir = os.path.join(savedir, f'{tcname}.jpg')   
    
# Save the plot as a high-quality figure
fig.savefig(savedir, bbox_inches='tight', format='jpg', dpi=450)
        