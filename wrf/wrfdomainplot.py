#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 16 14:19:51 2022

@author: sangdi
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 10:35:16 2021

@author: sangdi
"""
from scipy.interpolate import griddata
from scipy.interpolate import RectBivariateSpline
import glob
import datetime
import os
import math
import numpy as np
import pandas as pd
from netCDF4 import Dataset
import matplotlib.pylab as plt
import cartopy.crs as ccrs
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.feature as cfeature
import cartopy as cart
from matplotlib import colorbar, colors
from matplotlib.font_manager import FontProperties 
import matplotlib as mpl
import json
import codecs
import argparse

##variables
lon = [0]
lat = [0]
UAI = [0]



datadir = '/Users/sangdi/dust/wrfdomain/'
# datasto = '/data/disang/tropomi/dailydata/'


filelist = glob.glob(os.path.join(datadir,'*.nc'))


for file in filelist:
    filename = os.path.basename(file)

    
    
    nc_file = file
    fh1 = Dataset(nc_file, mode='r')
    ab = fh1['/ALBEDO12M'][:]
    # UVAI = fh1['/PRODUCT/aerosol_index_354_388'][:]
    # wd = fh.variables['owiWindDirection'][:]
    lons = fh1['XLONG_C'][:]
    lats = fh1['XLAT_C'][:]

    
    # data coordinates and values
    ab1 = ab[0,0,:,:]
    xs = ab1.shape[0]
    ys = ab1.shape[1]
    lons = lons[0,0:xs,0:ys]
    lats = lats[0,0:xs,0:ys]


lo = lons.flatten()
la = lats.flatten()
ab1= ab1.flatten()


## figure plot
fig = plt.figure(figsize=(12,7))

cmap1 = mpl.cm.turbo
bounds = [0,5,10,15,20,25,30]
norm = mpl.colors.BoundaryNorm(bounds, cmap1.N)



ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.set_extent([35, 95, 26, 63], crs=ccrs.PlateCarree())
# ax.set_extent([48, 63, 42.5, 49], crs=ccrs.PlateCarree())
# ax.set_extent([48, 56, 40, 48], crs=ccrs.PlateCarree())


### plot the frequency map
im = ax.tricontourf(lo,la,ab1,shading='flat', cmap=cmap1,transform=ccrs.PlateCarree())

# im = ax.pcolormesh(lons,lats,rf354_c,shading='flat', cmap=cmap1,transform=ccrs.PlateCarree())


ax.add_feature(cfeature.COASTLINE.with_scale('10m'),linewidth=.7,edgecolor='k',alpha=.5,zorder=100)
# ax.add_feature(states_provinces,linewidth=.3,linestyle='--',edgecolor='k',alpha=.5,zorder=100)
ax.add_feature(cfeature.LAKES.with_scale('10m'),linewidth=.7,facecolor='none',edgecolor='k',alpha=.5,zorder=100)
ax.add_feature(cfeature.BORDERS.with_scale('10m'),color='blue',linewidth=1,linestyle='--',edgecolor='k',alpha=.5,zorder=100)
# ax.set_title('sp',fontsize=14)

gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=.5, color='gray', alpha=0.5, linestyle='--')

gl.right_labels = False
gl.bottom_labels = None
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
gl.ylabel_style = {'size': 13,'color': 'black'}
gl.xlabel_style = {'size': 13,'color': 'black'}

cb3 = plt.colorbar(im, cmap=cmap1,fraction=0.07, pad=0.045,aspect=15,
                                extend='max',
                                extendfrac='auto',
                                spacing='uniform',
                                orientation='horizontal')
cb3.set_label('surface albedo')

plt.show()
