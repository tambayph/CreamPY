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
from matplotlib.patheffects import withStroke
from adjustText import adjust_text  # Import the adjust_text function
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

####### Only change this part #######
tcid = '7'
category = 'Typhoon'
tcname = 'Goring'
year = '2023'
tcbnumber = '1'
date = '11:00 AM, 16 August'
intname = '{}'
####### Only change this part #######

###################################################

gdfdir = f'D:/Ezra/Python/Test/Signals/JSON/{tcname}.json'
sdfdir = 'Edited_Province.json'
dfdir = f'D:/Ezra/Python/Test/Tracks/{year}/PH{year}0{tcid}.txt'
savedir = f'D:/Ezra/Python/Test/Output/{tcname}.jpg'

############### Download API #####################
url = f'http://10.10.1.97/fast/api/highest-signal/?id={year}{tcid}'

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

ymin = lowest_lat - 1
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

###############################################################################
#ADD LABEL
###############################################################################  
# Keep track of unique labels
unique_labels = set()

# Create a list to store label artists
label_artists = []

# Add labels to the plot
for idx, row in gdf.iterrows():
    label = row["ADM2_EN"]
    signal = row["Signals"]

    # Check if the label has already been plotted or if there is no signal value
    if label in unique_labels or signal is None:
        continue  # Skip this iteration if label already exists or no signal value

    unique_labels.add(label)  # Add the label to the set of unique labels
    
    # Check if the geometry is Polygon or MultiPolygon
    if row['geometry'].geom_type == 'Polygon':
        point = row['geometry'].centroid
    else:
        point = row['geometry'].representative_point()
    
    x, y = point.x, point.y
    
    # Define the white outline effect
    white_outline = withStroke(linewidth=3, foreground="white")
     
    # Annotate the point with the outlined label
    label_artist = ax.annotate(label, (x, y), color='black', path_effects=[white_outline])
    label_artists.append(label_artist)  # Add the label artist to the list

# Use adjust_text to optimize label positioning and avoid overlap
adjust_text(label_artists, ax=ax, autoalign='xy', only_move={'points':'xy', 'text':'xy'}, arrowprops=dict(arrowstyle="->", color='r', lw=0.8))


###############################################################################
#ADD TXTBOX
###############################################################################  
# Add a white rectangle patch at the bottom of the figure
rect = mpatches.Rectangle((0, 0), 1, 0.08, facecolor='white', transform=ax.transAxes)
ax.add_patch(rect)

# Add text on the rectangle patch
text = 'PAGASA-DOST'
ax.text(0.83, 0.04, text, color='black', fontsize=20, fontweight='bold', ha='left', va='center', transform=ax.transAxes)


# Add text on the rectangle patch
text = f'Tropical Cyclone Bulletin #{tcbnumber} - {category} "{tcname}" {intname}'

ax.text(0.65, 0.045, text, color='black', fontsize=20, fontweight='bold', ha='right', va='center', transform=ax.transAxes)

# Add text on the rectangle patch
text1 = f'{date} {year}'
ax.text(0.41, 0.025, text1, color='black', fontsize=20, ha='right', va='center', transform=ax.transAxes)

# Load the logo image
logo_img = plt.imread('D:/Ezra/Python/Test/PAGASA_Logo.svg_.png')  # Replace with the path to your PNG image

# Calculate the width of the logo in axes coordinates
logo_width = 0.1 * logo_img.shape[1] / fig.dpi

# Add pagasa-logo2 PNG image on the most right of the rectangle patch
logo_box = OffsetImage(logo_img, zoom=0.08)
logo_ab = AnnotationBbox(logo_box, (1 - logo_width, 0.04), frameon=False,
                         xycoords='axes fraction', boxcoords="axes fraction", pad=0.0)
ax.add_artist(logo_ab)
###############################################################################
#SAVE
###############################################################################    
# Save the plot as a high-quality figure
fig.savefig(savedir, bbox_inches='tight', format='jpg', dpi=450)
        