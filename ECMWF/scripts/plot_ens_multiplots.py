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
indir = f'{dts}/{init}'


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
    # val = np.load(f'{indir}/ecmwf_ens_ptile_{init_date:%Y%m%d%H}_f{fhour:03d}_{init_date+timedelta(hours=fhour):%Y%m%d%H}.npy')
    val = np.load('data/e1/202307200000/ecmwf_ens_ptile_2023072000_f144_2023072600.npy')


    ### Open lat, lon numpy files
    lat = np.load('scripts/ecmwf_lats.npy')
    lon = np.load('scripts/ecmwf_lons.npy')
    
    
    ### Initialize Figure with nrowsxncols subplots
    fig, axs = plt.subplots(ncols=3, nrows=2, subplot_kw={'projection': ccrs.PlateCarree()}, figsize=(12,6), dpi=150)
    
    ### adjust spacing between plots
    plt.subplots_adjust(hspace=0.3, wspace=0.3)
    
    
    ### ptile data label
    ptile_lab = ['p10', 'p25','p50', 'p75', 'p90', 'p99']    
    
    
    ### initialize counter to call ptile data
    j=0
    
    ### create plots for each rowxcol
    for row in list(range(2)):
        for col in list(range(3)):
            ax = axs[row,col]
    
            ### Set map projection, extents and plot coastlines
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
            clevs = [0.01,1.0,2.5,5.0,7.5,10,15,20,30]
            ccols = ['#ffffff','#d9d9d9','#cccccc','#8cb2ff','#899bfa','#fefe1b','#feec19','#ffc20a','#ff9e0c','#fa3c3c']
            cmap = mpl.colors.ListedColormap(ccols)
            

            ### Plot parameter with pcolormesh
            plot = ax.pcolormesh(lon, lat, val[j], cmap=cmap, shading='nearest', norm = mpl.colors.BoundaryNorm(clevs, ncolors=cmap.N, extend='both'))

            ### Plot subplot title text
            ax.set_title(f'{ptile_lab[j]}', loc='left', fontsize=12, pad=8)
            
            
            ### update counter to call ptile data
            j += 1

            
    ### Initialize and plot colorbar
    cbar = plt.colorbar(plot, ticks=clevs, ax=axs[:], orientation='vertical', drawedges=True, extendfrac='auto', extend='both', shrink=0.5)
    cbar.ax.tick_params(length=0, direction='out', color='black', labelsize=10, labelcolor='black')
    cbar.outline.set_linewidth(0.5)
    
    
    ### Plot figure text
    fig.suptitle(f'ECMWF IFS ENS 0.1deg {i}-Hour Accumulated Rainfall Percentile\n{init_date+timedelta(hours=8)+timedelta(hours=fhour-i):%I%p %a %b-%d} to {init_date+timedelta(hours=8)+timedelta(hours=fhour):%I%p %a %b-%d} [T+{fhour:03d}]\nInitialization: {init}Z', x=axs[0,0].get_position().x0, y=axs[0,0].get_position().y1+0.05, ha='left', va='bottom', fontsize=12)
    
    
    ### Save plot as image
    plt.savefig(f'{outdir}/ecmwf_ens_ptile_pcp_{init_date:%Y%m%d%H}_f{fhour:03d}_{init_date+timedelta(hours=fhour-i):%Y%m%d%H}_to_{init_date+timedelta(hours=fhour):%Y%m%d%H}.png', dpi=150, bbox_inches='tight')
    
    
    ### Close figure
    plt.close(fig)
    