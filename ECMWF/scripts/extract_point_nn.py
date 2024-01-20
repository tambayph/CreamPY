#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 13:50:48 2024

@author: nms
"""

### import libraries / modules

import os

import pygrib

from datetime import datetime as dt, timedelta
import numpy as np
import pandas as pd



### open stations csv file
stations = pd.read_csv('/home/nms/ecmwf/scripts/stations.csv')


### Initialization datetime
init = '202307200000'
init_date = dt.strptime(init,'%Y%m%d%H%M')


### Data Stream and Input directory
dts = 'a2'
indir = f'/home/nms/ecmwf/data/{dts}/{init}'


### List valid forecast hours
# fhours = list(range(1,90+1,1)) + list(range(93,144+3,3)) + list(range(150,168+6,6))
fhours = [144]


### Create output directory
outdir = f'/home/nms/ecmwf/hres/{dts}/{init}/station'
os.makedirs(outdir, exist_ok=True)



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

    
    ### Create dataframe of nearest neighbour point value for each station
    df_stn_nn = pd.DataFrame(columns=['staID','staName','sta_lon','sta_lat','ecm_lon','ecm_lat','pcp'])
    
    ### get nearest neighbour point value for each station
    for i in range(len(stations)):
        ## get index of latlon for each station wrt to grid data
        abslat = np.abs(lat-stations['lat'][i])
        abslon = np.abs(lon-stations['lon'][i])
        c = np.maximum(abslon,abslat)
        latlon_idx = np.argmin(c)
        x, y = np.where(c == np.min(c))
        
        ## get station nn latlon 
        ecm_lon_nn = np.around(lon[x[0],y[0]],decimals=6)
        ecm_lat_nn = np.around(lat[x[0],y[0]],decimals=6)
        
        ## get nn point value using index of station nn latlon 
        ecm_val_nn = np.around(val[x[0],y[0]],decimals=6)
        
        ## create dict of values
        df_nn = {'staID': stations['id'][i], 'staName': stations['staName'][i], 'sta_lon': stations['lon'][i], 'sta_lat': stations['lat'][i], 'ecm_lon': ecm_lon_nn, 'ecm_lat': ecm_lat_nn, 'pcp': ecm_val_nn}

        ## append dict of values to dataframe
        df_stn_nn = pd.concat([df_stn_nn, pd.DataFrame([df_nn])], ignore_index=True)
        

    ### save dataframe of nn values
    df_stn_nn.to_csv(f'{outdir}/ecmwf_pcp_nn_{init_date:%Y%m%d%H}_f{fhour:03d}_{init_date+timedelta(hours=fhour-i):%Y%m%d%H}_to_{init_date+timedelta(hours=fhour):%Y%m%d%H}.csv', index=False)
