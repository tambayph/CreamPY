# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 16:44:30 2023

@author: WF026
"""
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Read in the GeoJSON file
gdf = gpd.read_file('D:/Ezra/Python/Test/json per TC/01 Auring.json')
sdf = gpd.read_file('D:/Ezra/Python/Test/Data/Edited_Province.json')

# Define the frequency values and corresponding colors
color_dict = {'1': '#00CCFF', '2': '#FFFF00', '3': '#FFC000', '4': '#FF0000', '5': '#FF00FF'}

# Define a function to return the color for each value
def get_color(value):
    return color_dict.get(str(value), '#73b273')

# # Read the data from the text file
# df = pd.read_csv('D:/Ezra/Python/Test/Data/PH2021/PH202101.txt', sep='\s+', names=['col1', 'lat', 'lon', 'col4', 'col5', 'col6'], skiprows=1)

# # Convert the coordinates to decimal degrees format
# df['lat'] = df['lat'] / 10.0
# df['lon'] = df['lon'] / 10.0
# df['lat'] = df['lat'].round(1)
# df['lon'] = df['lon'].round(1)

# # Create a new column with the combined coordinates
# df['coords'] = list(zip(df['lat'], df['lon']))

# Plot the GeoDataFrame with custom colors
fig, ax = plt.subplots(figsize=(10, 10))
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
ax.legend(handles=handles, labels=labels, loc='upper left', title='Legend', title_fontsize=14)

# Set the background color of the legend frame to black
ax.get_legend().get_frame().set_facecolor('black')

ax.get_legend().get_title().set_color('white')

# Set the font color of the legend labels to white
for text in ax.get_legend().get_texts():
    text.set_color("white")

# Add sdf as a transparent overlay
sdf.plot(ax=ax, facecolor='none', edgecolor='black', alpha=1)

# Overlay the line from the text file on top of the plot
ax.plot(df['lon'], df['lat'], color='white', lw=2)

# Save the plot as a high-quality figure
fig.savefig('D:/Ezra/Python/Test/test.jpg', format='jpg', dpi=300)