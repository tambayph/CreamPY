# -*- coding: utf-8 -*-
"""
Created on Wed May 10 20:17:08 2023

@author: WF026
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 09:28:05 2023

@author: WF026
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

gdfdir = 'D:/Ezra/Python/Test/Falcon.json'
sdfdir = 'D:/Ezra/Python/Test/Data/Edited_Province.json'
dfdir = 'D:/Ezra/Python/Test/PH202306.txt'
savedir = 'D:/Ezra/Python/Test/Falcon.jpg'

# Original limitsy

xmin = 122
xmax = 123
ymin = 10
ymax = 22

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

# Read in the GeoJSON file
gdf = gpd.read_file(gdfdir)
sdf = gpd.read_file(sdfdir)

# Define the frequency values and corresponding colors
color_dict = {'1': '#00CCFF', '2': '#FFFF00', '3': '#FFC000', '4': '#FF0000', '5': '#FF00FF'}

# Define a function to return the color for each value
def get_color(value):
    return color_dict.get(str(value), '#73b273')

# Read the data from the text file
df = pd.read_csv(dfdir, sep='\s+', names=['col1', 'lat', 'lon', 'col4', 'col5', 'col6'], skiprows=1)

# Convert the coordinates to decimal degrees format
df['lat'] = df['lat'] / 10.0
df['lon'] = df['lon'] / 10.0
df['lat'] = df['lat'].round(1)
df['lon'] = df['lon'].round(1)

# Create a new column with the combined coordinates
df['coords'] = list(zip(df['lat'], df['lon']))

# Plot the GeoDataFrame with custom colors
fig, ax = plt.subplots(figsize=(17, 22), dpi=150)
gdf.plot(ax=ax, column='Signals', color=[get_color(value) for value in gdf['Signals']])

# Remove the numbers on the axis
ax.set_xticks([])
ax.set_yticks([])

# Set the background color
ax.set_facecolor('#002673')

# Create legend handles and labels
handles = [mpatches.Patch(color=color_dict[str(i)], label='TCWS #' + str(i)) for i in range(5, 0, -1)]
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

# Overlay the line from the text file on top of the plot
ax.plot(df['lon'], df['lat'], color='white', lw=4)


# set the new limits for the plot
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
# ax.set_aspect((xmax - xmin) / (ymax - ymin) * 6/4)

# Save the plot as a high-quality figure
fig.savefig(savedir, bbox_inches='tight', format='jpg', dpi=450)
