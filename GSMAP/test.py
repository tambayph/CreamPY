import matplotlib.pyplot as plt
import numpy as np

# Sample data
lon_map = np.linspace(-180, 180, 100)
lat_map = np.linspace(-90, 90, 50)
lon_map, lat_map = np.meshgrid(lon_map, lat_map)
rainfall = np.random.rand(50, 100)

# Create a plot
fig, ax = plt.subplots()
cmap = 'viridis'
norm = plt.Normalize(vmin=0, vmax=1)
cs = ax.pcolormesh(lon_map, lat_map, rainfall, cmap=cmap, norm=norm, label='Rainfall')

# Add a colorbar
cb = plt.colorbar(cs, ax=ax, orientation='vertical', label='Rainfall Intensity')

# Add a legend
ax.legend()

# Show the plot
plt.show()
