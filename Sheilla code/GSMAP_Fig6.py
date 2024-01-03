# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 15:08:33 2023

@author: WF026
"""

import gzip
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Path, PathPatch
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import ListedColormap
import os

########################################################################################################################
# File name of the chart for CODE1
save_name = 'D:/Ezra/Python/Test/Fig.6.png'

# Path of the directory for CODE1
path1 = 'D:/Ezra/PAGASA/Tropical Cyclone/GSMAP/GSMAP per TC'

# Path of the directory for CODE2
path2 = 'D:/Ezra/PAGASA/Tropical Cyclone/GSMAP/GSMAP data/2021'

########################################################################################################################
# Store the files in a list for CODE1
files1 = []

for (root,dirs,file) in os.walk(path1):
    for f in file:
        if '.gz' in f:
            files1.append(os.path.join(root, f))

accu_rr1 = np.zeros(4320000)

for i, file in enumerate(files1):
    gz = gzip.GzipFile(file, 'rb')
    rr = np.frombuffer(gz.read(), dtype=np.float32)
    rr = np.where(rr == -999.9, 0, rr)
    accu_rr1 = accu_rr1 + rr

rainfall1 = accu_rr1.reshape((1200, 3600))

# Store the files in a list for CODE2
files2 = []

for (root,dirs,file) in os.walk(path2):
    for f in file:
        if '.gz' in f:
            files2.append(os.path.join(root, f))

accu_rr2 = np.zeros(4320000)

for i, file in enumerate(files2):
    gz = gzip.GzipFile(file, 'rb')
    rr = np.frombuffer(gz.read(), dtype=np.float32)
    rr = np.where(rr == -999.9, 0, rr)
    accu_rr2 = accu_rr2 + rr

rainfall2 = accu_rr2.reshape((1200, 3600))

# Take the quotient of the two rainfalls
rainfall_quotient = (rainfall1 / rainfall2) * 100

########################################################################################################################
## PLOT

longitude=np.linspace(0.05, 359.95, 3600)
latitude=np.linspace(59.95, -59.95, 1200)

xmesh_model, ymesh_model = np.meshgrid(longitude, latitude, sparse=False)

fig, ax = plt.subplots(figsize=(8,8))

m = Basemap(llcrnrlat=4.5,urcrnrlat=24,llcrnrlon=113,urcrnrlon=128,lat_ts=20,resolution='h')
m.readshapefile('Provinces','Provinces')

#Draw boundaries
m.drawcoastlines(linewidth=0.6)
m.drawstates(linewidth=0.6)
m.drawcountries(linewidth=0.6)

#Convert to basemap projection scale
lon_map, lat_map = m(xmesh_model, ymesh_model)

# color scheme of the rainfall data
rgb = [[255,255,255],[204,204,255,255],[153,153,255,255],[51,102,255,255],[0,0,255,255],[51,102,255,255],[0,0,51,255],[204,119,255,255],[124,0,218,255],[255,0,214,255]]
rgb=np.array(rgb)/255.
cmap = ListedColormap(rgb,"")
boundaries = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
norm = matplotlib.colors.BoundaryNorm(boundaries, cmap.N, clip=True)

# Plot the rainfall on the basemap
cs = ax.pcolormesh(lon_map,lat_map,rainfall_quotient, cmap=cmap, norm=norm)

# Legend underneath the figure
cbaxes = fig.add_axes([0.164, 0.06, 0.7, 0.02])

cbar = fig.colorbar(cs, pad="5%", orientation="horizontal",
                    ticks=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100], cax=cbaxes)
cbar.ax.set_xticklabels(['0', '10', '20', '30', '40', '50', '60', '70',  '80', '90', '100'], fontsize=6.5)
cbar.set_label('mm', size=8)
cbar.ax.tick_params(size=0)

#######################################################################################################################
# Mask the ocean

#Getting the limits of the map:
x0,x1 = ax.get_xlim()
y0,y1 = ax.get_ylim()
map_edges = np.array([[x0,y0],[x1,y0],[x1,y1],[x0,y1]])

#Getting all polygons used to draw the coastlines of the map
polys = [p.boundary for p in m.landpolygons]

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

########################################################################################################################
#Save the figure

plt.savefig(save_name,bbox_inches='tight', pad_inches=0.1, dpi=400)
plt.close()