#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 13:28:38 2024

@author: nms
"""

### import libraries / modules

import os

from datetime import datetime as dt, timedelta

import numpy as np
import pygrib


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
outdir = f'/home/nms/ecmwf/hres/{dts}/{init}'
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
    
    
    
    # ### Open gribfile, select parameter, extract and process data values
    # ## without pre-processing
    # file = f'A2D{init_date:%m%d%H00}{init_date+timedelta(hours=fhour):%m%d%H00}1'
    # print(f'filename: {file}')
    
    # grbs = pygrib.open(f'{indir}/{file}')
    # grb = grbs.select(shortName='tp')[0]
    # print(grb)
    
    
    ### Open gribfile, select parameter, extract and process data values
    ## with pre-processing
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
        
    
    ### Save grid data as a numpy array file
    np.save(f'{outdir}/ecmwf_hres_pcp_{init_date:%Y%m%d%H}_f{fhour:03d}_{init_date+timedelta(hours=fhour-i):%Y%m%d%H}_to_{init_date+timedelta(hours=fhour):%Y%m%d%H}.npy', val)
