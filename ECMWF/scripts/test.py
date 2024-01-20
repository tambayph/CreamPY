### import libraries / modules
import os
import pygrib
from datetime import datetime as dt, timedelta
import numpy as np
import geopandas as gpd
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

### Initialization datetime
init = '202307200000'
init_date = dt.strptime(init, '%Y%m%d%H%M')

### Data Stream and Input directory
dts = 'a2'
indir = f'data/{dts}/{init}'

### List valid forecast hours
fhours = list(range(1,90+1,1)) + list(range(93,144+3,3)) + list(range(150,168+6,6))

### Loop through valid forecast hours to create plot
for fhour in fhours:
    ### Get forecast hour interval
    if fhour in list(range(1,90+1,1)):
        i=1
    elif fhour in list(range(93,144+3,3)):
        i=3
    elif fhour in list(range(150,168+6,6)):
        i=6
    print(f'i:{i}, forecast hour: {fhour}')

    ### Open gribfile, select parameter, extract and process data values
    if fhour==1:
        file_i = f'A2D{init_date:%m%d%H00}{init_date+timedelta(hours=fhour):%m%d%H00}1'
        grbs_i = pygrib.open(f'{indir}/{file_i}')
        grb_i = grbs_i.select(shortName='tp')[0]
        val = grb_i.values*1000.0

    else:
        file_i = f'A2D{init_date:%m%d%H00}{init_date+timedelta(hours=fhour):%m%d%H00}1'
        grbs_i = pygrib.open(f'{indir}/{file_i}')
        grb_i = grbs_i.select(shortName='tp')[0]        
        file_o = f'A2D{init_date:%m%d%H00}{init_date+timedelta(hours=fhour-i):%m%d%H00}1'
        grbs_o = pygrib.open(f'{indir}/{file_o}')
        grb_o = grbs_o.select(shortName='tp')[0]
        val = (grb_i.values*1000.0) - (grb_o.values*1000.0)
    
    ### Extract lat, lon values
    lat, lon = grb_i.latlons()    

        ### Initialize Figure
    fig = plt.figure(figsize=(12,12), dpi=70)

    ### Set map projection, extents and plot coastlines
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.spines['geo'].set_linewidth(0.5)
    ax.set_ylim((lat[-1,::][0], lat[0,::][0]))
    ax.set_xlim((lon[::,0][0], lon[::,-1][0]))
    ax.coastlines(resolution='10m', color='black', linewidth=0.5)