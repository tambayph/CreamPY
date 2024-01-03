# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 16:44:30 2023

@author: WF026
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Read in the GeoJSON file
gdf = gpd.read_file('D:/Ezra/Python/Test/Data/Municipal_Frequency.json')
sdf = gpd.read_file('D:/Ezra/Python/Test/Data/Edited_Province.json')

# Define the frequency values and corresponding colors
color_dict = {'1': '#ffff54', '2': '#66ff33', '3': '#33cc33', '4': '#0070c0', '5': '#003399', '6': '#003399', '7': '#003399', '8': '#003399'}

# Define a function to return the color for each value
def get_color(value):
    return color_dict.get(str(value), 'white')

# Plot the GeoDataFrame with custom colors
fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(ax=ax, column='Frequency', color=[get_color(value) for value in gdf['Frequency']])

# Remove the numbers on the axis
ax.set_xticks([])
ax.set_yticks([])

# Set the background color
ax.set_facecolor('white')

# Create legend handles and labels
legend_label = ['5 or higher', '4', '3', '2', '1']
handles = [mpatches.Patch(color=color_dict[str(i)], label= str(i)) for i in range(5, 0, -1)]

# Add legend to the plot
ax.legend(handles=handles, labels=legend_label, loc='upper left', title='Legend', title_fontsize=14)

# Set the background color of the legend frame to black
ax.get_legend().get_frame().set_facecolor('white')

ax.get_legend().get_title().set_color('black')

# Set the font color of the legend labels to white
for text in ax.get_legend().get_texts():
    text.set_color("black")

# Add sdf as a transparent overlay
sdf.plot(ax=ax, facecolor='none', edgecolor='black', alpha=1)
    
# Save the plot as a high-quality figure
fig.savefig('D:/Ezra/Python/Test/Frequency_2021.jpg', format='jpg', dpi=300)