# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 14:10:43 2023

@author: WF026
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 09:13:31 2023

@author: WF026
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

# Set the directory path
dir_path = 'D:/Ezra/Python/Test/'

# Loop through all files in the directory
for filename in os.listdir(dir_path):
    if filename.endswith('.json'):
        # Read in the GeoJSON file
        gdf = gpd.read_file(os.path.join(dir_path, filename))
        sdf = gpd.read_file('D:/Ezra/Python/Test/Data/Edited_Province.json')

        # Define the frequency values and corresponding colors
        color_dict = {'1': '#00CCFF', '2': '#FFFF00', '3': '#FFC000', '4': '#FF0000', '5': '#FF00FF'}

        # Define a function to return the color for each value
        def get_color(value):
            return color_dict.get(str(value), '#73b273')

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

        # Save the plot as a high-quality figure with the same name as the input file
        fig.savefig(os.path.join(dir_path, filename[:-5] + '.jpg'), format='jpg', dpi=300)

