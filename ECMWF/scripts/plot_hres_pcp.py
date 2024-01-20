# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

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
init_date = dt.strptime(init,'%Y%m%d%H%M')


### Data Stream and Input directory
dts = 'a2'
indir = f'data/{dts}/{init}'


### List valid forecast hours
# fhours = list(range(1,90+1,1)) + list(range(93,144+3,3)) + list(range(150,168+6,6))
# fhours = list(range(84,90+1,1)) + list(range(93,144+3,3))
fhours = [144]


### Plot Domain Extents
## selected domain
dom = 'whole_dom'

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


### Initialize Philippine provinces shapefile
ph_shp = gpd.read_file('shapefiles/ph_province/province_laglake.shp')



### Loop through valid forecast hours to create plot
for fhour in fhours:
    ### Get forecast hour interval
    if fhour in list(range(1,90+1,1)):
        i=1
    elif fhour in list(range(93,144+3,3)):
        i=3
    elif fhour in list(range(150,168+6,6)):
        i=6
    print(i,fhour)
    
    
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
    fig = plt.figure(figsize=(12,12), dpi=100)
    
    
    ### Set map projection, extents and plot coastlines
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_ylim((lat[-1,::][0], lat[0,::][0]))
    ax.set_xlim((lon[::,0][0], lon[::,-1][0]))
    # ax.set_ylim(extents[dom]['y'])
    # ax.set_xlim(extents[dom]['x'])
    ax.spines['geo'].set_linewidth(0.5)                                 
    ax.coastlines(resolution='10m', color='black', linewidth=0.5)
    
    
    ### Plot PH provinces
    ph_shp.plot(ax=ax, facecolor='none', edgecolor='#222222', linewidth=0.3, zorder=2)    
    
    
    ### Plot grid lines and labels
    gl = ax.gridlines(draw_labels=True, linestyle=':', linewidth=0.0, color='black')
    gl.top_labels = False
    gl.right_labels = False
    gl.xlocator = mticker.FixedLocator(list(np.arange(100,165,5)))
    gl.ylocator = mticker.FixedLocator(list(np.arange(-5,45,5)))
    # gl.xlocator = mticker.FixedLocator(list(np.arange(gls[dom][3],gls[dom][4],gls[dom][0])))
    # gl.ylocator = mticker.FixedLocator(list(np.arange(gls[dom][1],gls[dom][2],gls[dom][0])))
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'size': 10, 'color': 'black'}
    gl.ylabel_style = {'size': 10, 'color': 'black'}
    
    
    ### Set colormap contour levels and colors: Accumulated Rainfall
    clevs = [0.01,1.0,2.5,5.0,7.5,10,15,20,30]
    ccols = ['#ffffff','#d9d9d9','#cccccc','#8cb2ff','#899bfa','#fefe1b','#feec19','#ffc20a','#ff9e0c','#fa3c3c']
    cmap = mpl.colors.ListedColormap(ccols)
    
    
    ### Plot parameter with pcolormesh
    plot = ax.pcolormesh(lon, lat, val, cmap=cmap, shading='nearest', norm = mpl.colors.BoundaryNorm(clevs, ncolors=cmap.N, extend='both'))
    
    
    ### Initialize and plot colorbar
    cbax = fig.add_axes([ax.get_position().x1+0.02,ax.get_position().y0,0.011,ax.get_position().height])
    cbar = plt.colorbar(plot, ticks=clevs, cax=cbax, orientation='vertical', drawedges=True, extendfrac='auto', extend='both')
    cbar.ax.tick_params(length=0, direction='out', color='black', labelsize=10, labelcolor='black')
    cbar.outline.set_linewidth(0.5)
    
    
    ### Plot title text
    ax.set_title(f'ECMWF IFS 0.1deg\n{i}-Hour Accumulated Rainfall (mm)', loc='left', fontsize=12, pad=8)
    ax.set_title(f'{init_date+timedelta(hours=8)+timedelta(hours=fhour-i):%I%p %a %b-%d} to {init_date+timedelta(hours=8)+timedelta(hours=fhour):%I%p %a %b-%d} [T+{fhour:03d}]\nInitialization: {init}Z', loc='right', fontsize=12, pad=8)
    
    
    ### Save plot as image
    plt.savefig(f'{outdir}/ecmwf_tp_{init_date:%Y%m%d%H}_f{fhour:03d}_{init_date+timedelta(hours=fhour-i):%Y%m%d%H}_to_{init_date+timedelta(hours=fhour):%Y%m%d%H}', dpi=100, bbox_inches='tight')
    
    
    ### Close figure
    plt.close(fig)
    