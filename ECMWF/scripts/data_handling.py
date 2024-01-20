#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 13:16:28 2023

@author: nms3
"""

### import libraries / modules

### pygrib - for Grib data handling
import pygrib

### numpy - for Grib data manipulation
import numpy as np

### datetime - for datetime handling and manipulation
from datetime import datetime as dt, timedelta



###############################################################################

### filename
file = 'data/e1/202307200000/E1E07200000072000001'

### open a Grib file
grbs = pygrib.open(file)

### display total number of grib messages
grbs.messages

### display grib messages
grbs()

### select a grib message
grb = grbs[1]

### select grib message of a specific parameter
grb = grbs.select(shortName='tp')[0]

### list available keys of the grib data
grb.keys()

### extract data values only
val = grb.values

### extract lat and lon values only
lats, lons = grb.latlons()

### extract data, lat, lon values
val, lats, lons = grb.data()

### extract data, lat, lon values for a cropped area (ex. PAR)
val, lats, lons = grb.data(lat1=4, lat2=26, lon1=114, lon2=136)

### get analysis and valid datetime
grb.analDate

grb.validityDate

grb.validityTime



#### datetime

### To convert datetime object to string format, use strftime()
init = grb.analDate
init
init.strftime('%Y%m%d%H%M')
init.strftime('%I%p %a %b-%d')

### To convert to a different timezone, add time difference using timedelta
phst = init + timedelta(hours=8)
phst.strftime('%Y%m%d%H%M')
phst.strftime('%I%p %a %b-%d')

### To convert datetime object to string format, use f string formatting
init = grb.analDate
init
f'{init:%Y%m%d%H%M}'
f'{init + timedelta(hours=8):%Y%m%d%H%M}'

### To convert string to datetime object, use strptime()
valid = f'{grb.validityDate}{grb.validityTime:04d}'
valid
valid = dt.strptime(valid, '%Y%m%d%H%M')
valid



#### grid data pre-processing

### Precipitation
grb = grbs.select(shortName='tp')[0]
val = grb.values
np.max(val)
val = val * 1000.0
np.max(val)


### Temperature
grb = grbs.select(shortName='2t')[0]
val = grb.values
np.max(val)
val = val - 273.15
np.max(val)


### Mean sea level pressure
grb = grbs.select(shortName='msl')[0]
val = grb.values
np.max(val)
val = val / 100
np.max(val)


### Wind: get wind speed from u,v components
u = grbs.select(shortName='10u')[0].values
v = grbs.select(shortName='10v')[0].values
wspd = (u**2 + v**2) ** 0.5
wspd


### Total Precipitation: get only accumulation for the valid forecast period
grbs_i = pygrib.open('data/e1/202307200000/E1E07200000072000001')
grb_i = grbs_i.select(shortName='tp')[0]
val_i = grb_i.values*1000.0

grbs_o = pygrib.open('data/e1/202307200000/E1E07200000072000001')
grb_o = grbs_o.select(shortName='tp')[0]
val_o = grb_o.values*1000.0

val = val_i - val_o



#### For some parameters that are only available at specific forecast hours
grbs = pygrib.open('data/e1/202307200000/E1E07200000072000001')
grb = grbs.select(shortName='tp')[0]

grbs = pygrib.open('data/e1/202307200000/E1E07200000072000001')
grb = grbs.select(shortName='tp')[0]



#### Save grid data as a new grib file
grbs = pygrib.open('data/e1/202307200000/E1E07200000072000001')
grb = grbs.select(shortName='tp')[0]

msg = grb.tostring()

grbout = open('test.grb', 'wb')
grbout.write(msg)

