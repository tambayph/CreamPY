# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

### import libraries / modules
import os

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
init_date = dt.strptime(init,'%Y%m%d%H%M')


### Data Stream and Input directory
dts = 'e1'
indir = f'ens/{dts}/{init}'


### List valid forecast hours
# fhours = list(range(1,90+1,1)) + list(range(93,144+3,3)) + list(range(150,168+6,6))
# fhours = list(range(84,90+1,1)) + list(range(93,144+3,3))
fhours = [144]


### Plot Domain Extents
## selected domain
dom = 'PAR'

## extents of selected domain
extents = {'whole_dom'  : {'x': (100,160), 'y': (-5,40)},
           'PAR' : {'x':(115,135), 'y':(4,25)},
           'PH' : {'x':(116,128), 'y':(4,22)},
           }

## for gridlines and labels of selected domain
gls = {'whole_dom' : [5.0, -5, 40, 100, 160, 'gray'],
       'PAR': [2.0, 4, 26, 114, 136, 'gray'],
       'PH': [2.0, 4, 22, 116, 128, 'gray']
       }


### Create output directory
outdir = f'plot/{dts}/{init}/{dom}'
os.makedirs(outdir, exist_ok=True)


### Philippine provinces shapefile
ph_shp = gpd.read_file('shapefiles/ph_province/province_laglake.shp')




### Loop through valid forecast hours to create plot
for fhour in fhours:
    ### Get forecast hour interval
    if fhour in list(range(3,144+3,3)):
        i=3
    elif fhour in list(range(150,168+6,6)):
        i=6
    print(i,fhour)
    
    
    ### Open numpy file
    val = np.load(f'{indir}/ecmwf_ens_pqpf7.5_{init_date:%Y%m%d%H}_f{fhour:03d}_{init_date+timedelta(hours=fhour):%Y%m%d%H}.npy')


    ### Open lat, lon numpy files
    lat = np.load('scripts/ecmwf_lats.npy')
    lon = np.load('scripts/ecmwf_lons.npy')
    
    
    ### Initialize Figure
    fig = plt.figure(figsize=(12,12), dpi=100)
    
    
    ### Set map projection, extents and plot coastlines
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_ylim(extents[dom]['y'])
    ax.set_xlim(extents[dom]['x'])
    # ax.set_ylim((lat[-1,::][0], lat[0,::][0]))
    # ax.set_xlim((lon[::,0][0], lon[::,-1][0]))
    ax.spines['geo'].set_linewidth(0.5)                                 
    ax.coastlines(resolution='10m', color='black', linewidth=0.5)
    
    
    ### Plot PH provinces
    ph_shp.plot(ax=ax, facecolor='none', edgecolor='#222222', linewidth=0.3, zorder=2)    
    
    
    ### Plot grid lines and labels
    gl = ax.gridlines(draw_labels=True, linestyle=':', linewidth=0.0, color='black')
    gl.top_labels = False
    gl.right_labels = False
    gl.xlocator = mticker.FixedLocator(list(np.arange(gls[dom][3],gls[dom][4],gls[dom][0])))
    gl.ylocator = mticker.FixedLocator(list(np.arange(gls[dom][1],gls[dom][2],gls[dom][0])))
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'size': 10, 'color': 'black'}
    gl.ylabel_style = {'size': 10, 'color': 'black'}
    
    
    ### Set colormap contour levels and colors: PQPF
    clevs = [0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    ccols = ['#ffffff', '#d4d6d4', '#b4caff', '#8cb2ff', '#899bfa', '#a9d158',
             '#ebf4ac', '#fee518', '#ffd22c', '#ff9e0c', '#fc4e2a']
    cmap = mpl.colors.ListedColormap(ccols)
    
    
    ### Plot parameter with pcolormesh
    plot = ax.pcolormesh(lon, lat, val, cmap=cmap, shading='nearest', norm = mpl.colors.BoundaryNorm(clevs, ncolors=cmap.N, extend='neither'))
    
    
    ### Initialize and plot colorbar
    cbax = fig.add_axes([ax.get_position().x1+0.02,ax.get_position().y0,0.011,ax.get_position().height])
    cbar = plt.colorbar(plot, ticks=clevs, cax=cbax, orientation='vertical', drawedges=True, extendfrac='auto', extend='neither')
    cbar.ax.tick_params(length=0, direction='out', color='black', labelsize=10, labelcolor='black')
    cbar.outline.set_linewidth(0.5)
    
    
    ### Plot title text
    ax.set_title(f'ECMWF IFS ENS 0.1deg\n{i}-Hour PQPF > 7.5mm', loc='left', fontsize=12, pad=8)
    ax.set_title(f'{init_date+timedelta(hours=8)+timedelta(hours=fhour-i):%I%p %a %b-%d} to {init_date+timedelta(hours=8)+timedelta(hours=fhour):%I%p %a %b-%d} [T+{fhour:03d}]\nInitialization: {init}Z', loc='right', fontsize=12, pad=8)
    
    
    ### Save plot as image
    plt.savefig(f'{outdir}/ecmwf_ens_pqpf7.5_{init_date:%Y%m%d%H}_f{fhour:03d}_{init_date+timedelta(hours=fhour-i):%Y%m%d%H}_to_{init_date+timedelta(hours=fhour):%Y%m%d%H}.png', dpi=100, bbox_inches='tight')
    
    
    ### Close figure
    plt.close(fig)
    