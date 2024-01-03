import gzip
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Path, PathPatch
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import ListedColormap
import os
import glob
import pandas as pd
import glob

########################################################################################################################
#  File name of the chart
save_name = 'D:/Ezra/Python/Test/01 Amang.png'

# Path of the directory
path = 'D:/Ezra/PAGASA/GSMAP/2023/Amang'

########################################################################################################################
# Store the files in a list
files = []

for (root,dirs,file) in os.walk(path):
    for f in file:
        if '.gz' in f:
            files.append(os.path.join(root, f))

accu_rr = np.zeros(4320000)

for i, file in enumerate(files):
    gz = gzip.GzipFile(file, 'rb')
    rr = np.frombuffer(gz.read(), dtype=np.float32)
    rr = np.where(rr == -999.9, 0, rr)
    accu_rr = accu_rr + rr

rainfall = accu_rr.reshape((1200, 3600))

########################################################################################################################
## PLOT

rainfall=accu_rr.reshape((1200, 3600))
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
rgb = [[255,255,255],[128,255,2],[0,140,2],[255,255,0],[255,140,0],[255,0,0],[158,30,30],[255,0,214],[124,0,218]]
rgb=np.array(rgb)/255.
cmap = ListedColormap(rgb,"")
boundaries = [0, 100, 250, 500, 750, 1000, 1250, 1500, 2000, 1000000000]
norm = matplotlib.colors.BoundaryNorm(boundaries, cmap.N, clip=True)

# Plot the rainfall on the basemap
cs = ax.pcolormesh(lon_map,lat_map,rainfall, cmap=cmap, norm=norm)

# Legend underneath the figure
cbaxes = fig.add_axes([0.164, 0.06, 0.7, 0.02])

cbar = fig.colorbar(cs, pad="5%", orientation="horizontal",
                    ticks=[0, 100, 250, 500, 750, 1000, 1250, 1500,  2000, 500001000], cax=cbaxes)
cbar.ax.set_xticklabels([' ', '100', '250', '500', '750', '1000', '1250', '1500',  '2000', ' '], fontsize=6.5)
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
plt.show()