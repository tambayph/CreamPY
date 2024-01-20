#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 13:29:03 2024

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
dts = 'e1'
indir = f'data/{dts}/{init}'


### List valid forecast hours
# fhours = list(range(3,144+3,3)) + list(range(150,168+6,6))
fhours = [144]


### Create output directory
outdir = f'ens/{dts}/{init}'
os.makedirs(outdir, exist_ok=True)



### Loop through valid forecast hours to create plot
for fhour in fhours:
    ### Get forecast hour interval
    if fhour in list(range(3,144+3,3)):
        i=3
    elif fhour in list(range(150,168+6,6)):
        i=6
    print(f'i:{i}, forecast hour: {fhour}')
    
    
    ### create empty list to append values for each ensemble member
    mval = []
    
    ### loop through each ensemble member and extract values
    if fhour==3:
        file_i = f'E1E{init_date:%m%d%H00}{init_date+timedelta(hours=fhour):%m%d%H00}1'
        grbs_i = pygrib.open(f'{indir}/{file_i}')

        for mem in range(0,51):
            print(f'member: {mem}')
            
            grb_i = grbs_i.select(shortName='tp', perturbationNumber=mem)[0]
            val = grb_i.values*1000.0

            mval.append(val)
    else:
        file_i = f'E1E{init_date:%m%d%H00}{init_date+timedelta(hours=fhour):%m%d%H00}1'
        grbs_i = pygrib.open(f'{indir}/{file_i}')

        file_o = f'E1E{init_date:%m%d%H00}{init_date+timedelta(hours=fhour-i):%m%d%H00}1'
        grbs_o = pygrib.open(f'{indir}/{file_o}')
        
        for mem in range(0,51):
            print(f'member: {mem}')
            
            grb_i = grbs_i.select(shortName='tp', perturbationNumber=mem)[0]
            grb_o = grbs_o.select(shortName='tp', perturbationNumber=mem)[0]
            
            val = (grb_i.values*1000.0) - (grb_o.values*1000.0)

            mval.append(val)
        
        
    ### create numpy array of values for each ensemble member
    mval = np.asarray(mval)
    
    
    
    ### mean of control + 50 ensemble members
    mean = np.nanmean(mval, axis=0)
    
    ## Save mean as numpy file
    np.save(f'{outdir}/ecmwf_emean_{init_date:%Y%m%d%H}_f{fhour:03d}_{init_date+timedelta(hours=fhour):%Y%m%d%H}.npy', mean)
    
    
    ### standard deviation
    std = np.nanstd(mval, axis=0)

    ## Save standard deviation as numpy file
    np.save(f'{outdir}/ecmwf_std_{init_date:%Y%m%d%H}_f{fhour:03d}_{init_date+timedelta(hours=fhour):%Y%m%d%H}.npy', std)
    
    
    ### percentile
    ptile = np.nanpercentile(mval, [10,25,50,75,90,99], axis=0)
    
    ## Save percentile as numpy file
    np.save(f'{outdir}/ecmwf_ens_ptile_{init_date:%Y%m%d%H}_f{fhour:03d}_{init_date+timedelta(hours=fhour):%Y%m%d%H}.npy', ptile)

    
    ### probability of exceedance
    thold = 7.5
    poe = np.nanmean(np.where(np.isnan(mval), mval, (mval >= thold).astype(int)), axis=0)
    
    ## Save poe as numpy file
    np.save(f'{outdir}/ecmwf_ens_pqpf{thold}_{init_date:%Y%m%d%H}_f{fhour:03d}_{init_date+timedelta(hours=fhour):%Y%m%d%H}.npy', poe)
