#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 22:34:43 2021

@author: sangdi
"""

from zipfile import ZipFile
import os
import glob
import datetime
from satpy import Scene
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from satpy.writers import get_enhanced_image
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import tarfile


### access the original zip files
zipfiles = sorted(glob.glob('/Users/sangdi/nat/MSG1*.zip'))

### extract the native files from the zip files
for ifile,file in enumerate(zipfiles):

    with ZipFile(file, 'r') as zipObject:
        listOfFileNames = zipObject.namelist()
        for fileName in listOfFileNames:
            if fileName.endswith('.nat'):
                # Extract a single file from zip
                zipObject.extract(fileName, '/Users/sangdi/nat/natf')

### access the native files                
natfiles = sorted(glob.glob('/Users/sangdi/nat/natf/MSG1*.nat'))


### aceess the time info from the name or extrcat time info directly from satpy "q"
for ifile,file in enumerate(natfiles):
    filename = os.path.basename(file)
    ### name example: MSG1-SEVI-MSG15-0100-NA-20180101001245.247000000Z-NA.nat###
    ### MSG1-SEVI-MSG15-0100-NA-20180101002745.391000000Z-NA.nat
    time1 = filename.split('-')[5]
    time = datetime.datetime.strptime(time1.split('.')[0],'%Y%m%d%H%M%S')
    
    scn = Scene(reader='seviri_l1b_native', filenames=[file])    
    scn.load(['dust'])
    q = scn['dust'].attrs['start_time']  #access time of the data
    ### q = scn['dust'].max().compute()   ##compute the maximum
    p = scn['dust'].coords['bands']
    ## # extract the lon lat info


    ## lons, lats = scn['dust'].attrs['area'].get_lonlats()

    ### plot with satpay
    crs = scn['dust'].attrs['area'].to_cartopy_crs()

    ax = plt.axes(projection = ccrs.PlateCarree())
    ax.set_extent([45, 85, 35, 56], crs=ccrs.PlateCarree())
    img = get_enhanced_image(scn['dust'])

    img_data = img.data
    img_data.plot.imshow(rgb='bands',vmin=0,vmax=1,transform=crs)
# ax.coastlines()

## ADD lakes and rivers
# ax.add_feature(cfeature.COASTLINE.with_scale('10m'))
# ax.add_feature(cfeature.RIVERS.with_scale('10m'))

    ax.add_feature(cfeature.COASTLINE.with_scale('10m'),linewidth=.5,edgecolor='k',alpha=.5,zorder=100)
    ax.add_feature(cfeature.LAKES.with_scale('10m'),linewidth=.5,facecolor='none',edgecolor='k',alpha=.5,zorder=100)
# ax.add_feature(cfeature.BORDERS.with_scale('10m'),linewidth=.5,edgecolor='k',alpha=.5,zorder=100)

    ax.set_title(time)
    ax.set_alpha(.95)
    plt.show()
    # plt.savefig(fname="/Users/sangdi/test/SEVIRI_{:s}.png".format(time.strftime('%Y%m%d%H%M%S')),dpi=800, bbox_inches='tight')