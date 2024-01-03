import gzip
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Path, PathPatch
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import ListedColormap
import pandas as pd
import os
########################################################################################################################

with open("input.txt", "r") as file:
    lines = file.readlines()
    selected_file_path = lines[0].strip()
    selected_file_dir = lines[1].strip()

# Input the filename
tcid = selected_file_path
tcname = selected_file_dir

########################################################################################################################
savedir = 'D:/Ezra/Python/Test/'+tcname

# OPEN THE FILES

# TC best track
track_fname = f'D:/Ezra/Python/Test/Tracks/2023/PH2023{tcid}.txt'

# Path of the directory of GSMAP files
path = f'D:/Ezra/PAGASA/GSMAP/2023/{tcname}/'

# Synop and Agromet RR observations
rr_obs = pd.read_csv(f'D:/Ezra/Python/Test/Rainfall/{tcname}.csv')
########################################################################################################################
# Store the files in a list
files = []

for (root,dirs,file) in os.walk(path):
    for f in file:
        if '.gz' in f:
            files.append(os.path.join(root, f))


# Open and read the file with extension .dat.gz
# The files are saved in the list gz
gz = [gzip.GzipFile(file,'rb') for file in files]
########################################################################################################################
# DATA PREPARATION

# Store the arrays in the list rr
rr = [np.frombuffer(gz[i].read(), dtype=np.float32) for i in range (0,len(gz))]

# Replace missing values(-999.9) with 0
rr = np.where(rr==-999.9,0,rr)

# Sum all the arrays in the list
accu_rr = sum(rr)

# Reshape
rainfall=accu_rr.reshape((1200, 3600))

# Observed rainfall from synop and agromet stations
lon = rr_obs['lon'].astype(float)
lat = rr_obs['lat'].astype(float)
obs_rr = rr_obs['Accumulated'].astype(float)
########################################################################################################################
longitude=np.linspace(0.05, 359.95, 3600)
latitude=np.linspace(59.95, -59.95, 1200)

xmesh_model, ymesh_model = np.meshgrid(longitude, latitude, sparse=False)

fig, axes = plt.subplots(nrows=1, ncols = 2, figsize=(8,6))

m = Basemap(llcrnrlat=4.5,urcrnrlat=24,llcrnrlon=113,urcrnrlon=128,lat_ts=20,resolution='h',ax = axes[0])
m.readshapefile('Provinces','Provinces')

#Draw boundaries
m.drawcoastlines(linewidth=0.6)
m.drawstates(linewidth=0.6)
m.drawcountries(linewidth=0.6)

#Convert to basemap projection scale
lon_map, lat_map = m(xmesh_model, ymesh_model)

# color scheme of the rainfall data
rgb = [[255,255,255],[186,184,184],[0,197,255],[107,251,144],[255,255,0],[255,170,0],[255,0,0],[255,115,223],[132,0,168]]
rgb=np.array(rgb)/255.
cmap = ListedColormap(rgb,"")
boundaries = [0,1, 10, 25, 50, 100, 200, 300, 500, 5000]
norm = matplotlib.colors.BoundaryNorm(boundaries, cmap.N, clip=True)

# Plot the rainfall on the basemap
cs = axes[0].pcolormesh(lon_map,lat_map,rainfall, cmap=cmap, norm=norm)

# Legend underneath the figure
cbaxes = fig.add_axes([0.189, 0.06, 0.647, 0.02])
cbar = fig.colorbar(cs, pad=0, orientation="horizontal",
                    ticks=[0,1, 10, 25, 50, 100, 200, 300, 500, 5000], cax=cbaxes)
cbar.ax.set_xticklabels([" ","1","10","25","50","100", "200", "300","500"," "], fontsize=7)
cbar.set_label('mm', size=8)
cbar.ax.tick_params(size=0)
########################################################################################################################
# Mask the ocean

#Getting the limits of the map:
x0,x1 = axes[0].get_xlim()
y0,y1 = axes[0].get_ylim()
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
axes[0].add_patch(patch)
########################################################################################################################
m2 = Basemap(llcrnrlat=4.5,urcrnrlat=24,llcrnrlon=113,urcrnrlon=128,lat_ts=20,resolution='h',ax = axes[1])
m2.readshapefile('Provinces','Provinces')

#Draw boundaries
m2.drawcoastlines(linewidth=0.6)
m2.drawstates(linewidth=0.6)
m2.drawcountries(linewidth=0.6)

axes[1].scatter(lon,lat,c = obs_rr, edgecolor='black', s= 25, linewidth =0.5, cmap=cmap, norm=norm,zorder=10)
########################################################################################################################
# Inset Metro Manila

axins = axes[1].inset_axes([0.03,0.5,0.3,0.2])
inmap = Basemap(llcrnrlat=4.5,urcrnrlat=24,llcrnrlon=115,urcrnrlon=128,lat_ts=20,resolution='h', ax=axins)
inmap.readshapefile('Provinces','Provinces')

axins.scatter(lon,lat,c = obs_rr, edgecolor='black', s= 40, linewidth =0.5, cmap=cmap, norm=norm,zorder=10)

x1,x2,y1,y2 = 120.7,121.3, 14.3, 14.85

axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
axins.set_xticklabels([])
axins.set_yticklabels([])
axes[1].indicate_inset_zoom(axins, edgecolor="black")
########################################################################################################################
# Add the TC track

# Used to prevent error in tokenizing data
names_temp = ['0','1','2','3','4','5','6','7']

best = pd.read_csv(track_fname, sep=' ', header=None, skiprows=[0], names=names_temp)

# Prepare the data
best.drop(['1','4'], inplace=True, axis=1)
best.columns = ['date', 'lat', 'lon', 'wind','pres', 'cat']
best['lat'] = best['lat'].astype(float)
best['lon'] = best['lon'].astype(float)
best['lat'] = best['lat'] * 0.1
best['lon'] = best['lon'] * 0.1

axes[0].plot(best['lon'],best['lat'],color='black',linewidth=1.5,zorder=5)

axes[1].plot(best['lon'],best['lat'],color='black',linewidth=1.5,zorder=5)
########################################################################################################################
# Save the figure
# Create the directory if it doesn't exist
if not os.path.exists(savedir):
    os.makedirs(savedir)

savedir = os.path.join(savedir, f'rr{tcname}.png')   

plt.subplots_adjust(hspace=0)
fig.tight_layout()
plt.savefig(savedir,bbox_inches='tight', pad_inches=0.1, dpi=400)
plt.close()
