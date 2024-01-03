import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import ListedColormap
import pandas as pd
from scipy.interpolate import griddata
from matplotlib.patches import Path, PathPatch
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.image as mpimg  # Import the image module
import requests
from scipy.ndimage import gaussian_filter
from matplotlib.patheffects import withStroke

###################################################################################################
num = '02'
date = f'202309{num}'
###################################################################################################

# Replace 'your_api_url_here' with the actual API URL that provides the JSON data.
api_url = f'http://10.11.1.107/api/rainfall/{date}0000'

# Send a GET request to the API
response = requests.get(api_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    data = response.json()

    # Create an empty DataFrame
    df = pd.DataFrame(columns=["#", "Name", "lat", "lon","RR"])

    # Iterate through the data and extract the required information
    for station in data:
        stn_number = station["stn_number"]
        stn_name = station["stn_name"]
        lat = station["lat"]
        lon = station["lon"]
        total_value = None

        for entry in station["rainfall"]:
            if entry["valueType"] == "total":
                total_value = entry["value"]

        df = df.append({"#": stn_number, "Name": stn_name, "lat": lat, "lon": lon, "RR": total_value}, ignore_index=True)

    # Save the DataFrame to a CSV file
    df.to_csv("output.csv", index=False)

    print("CSV file has been created: output.csv")

else:
    print("Failed to retrieve data from the API. Status code:", response.status_code)

# Load your CSV data
rr_obs = pd.read_csv('output.csv')

# Replace 'T' with '0' in the 'RR' column
rr_obs['RR'] = rr_obs['RR'].replace('T', '0')

# Convert the 'RR' column to numeric (assuming it contains numbers)
rr_obs['RR'] = pd.to_numeric(rr_obs['RR'])

# Rearrange the DataFrame based on the 'RR' column in descending order
rr_obs = rr_obs.sort_values(by='RR', ascending=False)

# Reset the index of the DataFrame if needed
rr_obs = rr_obs.reset_index(drop=True)

# Extract the latitude, longitude, and rainfall values
lon = rr_obs['lon'].astype(float)
lat = rr_obs['lat'].astype(float)
obs_rr = rr_obs['RR'].astype(float)

# Rearrange the DataFrame based on the 'RR' column in descending order
rr_obs_sorted = rr_obs.sort_values(by='RR', ascending=False)

# Create a grid of coordinates for interpolation
grid_lon = np.linspace(114, 127, 3600)
grid_lat = np.linspace(21, 5, 3600)
grid_lon, grid_lat = np.meshgrid(grid_lon, grid_lat, sparse=False)

# Interpolate rainfall values onto the grid using cubic interpolation
grid_rr = griddata((lon, lat), obs_rr, (grid_lon, grid_lat), method='linear')
# Apply Gaussian smoothing to the grid_rr
sigma = 5.0  # Adjust this parameter for the desired level of smoothing
smoothed_grid_rr = gaussian_filter(grid_rr, sigma=sigma, mode='constant', cval=np.nan)

# Plotting
fig, ax = plt.subplots(figsize=(10, 10))

m2 = Basemap(llcrnrlat=5, urcrnrlat=21, llcrnrlon=114, urcrnrlon=127, lat_ts=20, resolution='h', ax=ax)
m2.readshapefile('Provinces', 'Provinces')

# Draw boundaries
m2.drawcoastlines(linewidth=0.6)
m2.drawstates(linewidth=0.6)
m2.drawcountries(linewidth=0.6)

# Color scheme of the rainfall data with RGB values as floats
rgb = [
    [1.0, 1.0, 1.0],        # White
    [0.0, 0.772, 1.0],      # Light Blue
    [1.0, 1.0, 0.0],        # Yellow
    [1.0, 0.667, 0.0],      # Orange
    [1.0, 0.0, 0.0],        # Red
    [1.0, 0.451, 0.874],    # Pink
    [0.518, 0.0, 0.659]     # Purple
]

cmap = ListedColormap(rgb, "")
boundaries = [0, 1, 30, 60, 180, 360, 720, 5000]
norm = matplotlib.colors.BoundaryNorm(boundaries, cmap.N, clip=True)

# Plot the interpolated rainfall values
sc = ax.pcolormesh(grid_lon,grid_lat,grid_rr, cmap=cmap, norm=norm)

# Legend outside the figure
divider = make_axes_locatable(ax)
cax = divider.append_axes("bottom", size="2%", pad=0.1)

# Custom labels for color bar ticks
tick_labels = ['<1.0 (Trace)', 
               '30 (Very Light)', 
               '60 (Light)', 
               '180 (Moderate)', 
               '360 (Heavy)', 
               '720 (Intense)', 
               '>720 (Torrential)'
]

# Calculate positions for the tick labels in the middle of each color segment
tick_positions = [0.5 * (boundaries[i] + boundaries[i + 1]) for i in range(len(boundaries) - 1)]

# Plot the color bar with custom tick positions and labels
cbar = fig.colorbar(sc, cax=cax, orientation="horizontal", ticks=tick_positions)
cbar.ax.set_xticklabels(tick_labels, fontsize=8)
cbar.set_label('mm', size=10)
cbar.ax.tick_params(size=0)

# #######################################################################################################################
# Mask the ocean

#Getting the limits of the map:
x0,x1 = ax.get_xlim()
y0,y1 = ax.get_ylim()
map_edges = np.array([[x0,y0],[x1,y0],[x1,y1],[x0,y1]])

#Getting all polygons used to draw the coastlines of the map
polys = [p.boundary for p in m2.landpolygons]

#Combining with map edges
polys = [map_edges]+polys[:]

#Creating a PathPatch
codes = [
    [Path.MOVETO] + [Path.LINETO for p in p[1:]]
    for p in polys
]
polys_lin = [v for p in polys for v in p]
codes_lin = [c for cs in codes for c in cs]
path = Path(polys_lin, codes_lin)
patch = PathPatch(path,facecolor='white', lw=0)

#Masking the data:
ax.add_patch(patch)

#######################################################################################################################

# Add a small image
small_image = mpimg.imread('PAGASA_Logo.png')  # Replace 'small_image.png' with the path to your image
small_image_ax = fig.add_axes([0.13, 0.87, 0.1, 0.1])
small_image_ax.imshow(small_image)
small_image_ax.axis('off')  # Turn off axis for the small image

########################################################################################################################

# Add text in the upper-left corner
upper_left_text = f"24-HOUR ISOHYETAL ANALYSIS\nSeptember {num}, 2023"
fig.text(0.24, 0.91, upper_left_text, fontsize=12, color='blue', weight='bold')

# Add text in the upper-left corner
iso = "WFS-13 Rev.0/15-08-2023"
fig.text(0.68, 0.97, iso, fontsize=10, color='black', weight='bold')

# Add text in the upper-left corner
synop = "24-HOUR HIGHEST RAINFALL(mm)"
fig.text(0.14, 0.83, synop, fontsize=10, color='black', weight='bold')

# Assuming your data is stored in a DataFrame named 'rr_obs_sorted'
selected_data1 = rr_obs_sorted.iloc[:5, [0]]
selected_data2 = rr_obs_sorted.iloc[:5, [1]]
selected_data3 = rr_obs_sorted.iloc[:5, [4]]

desired_width = 30
# Left-align the text in the 'Location' column
selected_data2['Name'] = selected_data2['Name'].str.ljust(desired_width)
selected_data3['RR'] = selected_data3['RR'].astype(str)
selected_data3['RR'] = selected_data3['RR'].str.ljust(desired_width)

# Print the formatted DataFrame
text_representation1 = selected_data1.to_string(header=False, index=False)
text_representation2 = selected_data2.to_string(header=False, index=False)
text_representation3 = selected_data3.to_string(header=False, index=False)

fig.text(0.14, 0.76, text_representation1, fontsize=8, color='black', weight='bold')
fig.text(0.19, 0.76, text_representation2, fontsize=8, color='black', weight='bold')
fig.text(0.41, 0.76, text_representation3, fontsize=8, color='black', weight='bold')

# Define the white outline effect
outline_effect = [withStroke(linewidth=3, foreground='white')]

# Annotate points with RR values
for i, rr in enumerate(obs_rr):
    ax.annotate(f'{rr:.1f}', (rr_obs['lon'][i], rr_obs['lat'][i]), fontsize=8, color='black',
                alpha=0.7, path_effects=outline_effect)    
########################################################################################################################
#Save the figure

fig.tight_layout()
plt.savefig(f'{date}.png', bbox_inches='tight', pad_inches=0.1, dpi=600)
plt.show()
