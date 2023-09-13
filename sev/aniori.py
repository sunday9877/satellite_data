#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 28 14:14:32 2021

@author: sangdi
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 20 11:02:51 2021

@author: sangdi
"""

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
import imageio
# from pygifsicle import optimize

#from pyresample import geometry

import warnings
warnings.filterwarnings("ignore")

# my_tar = tarfile.open('/Users/sangdi/Downloads/1511888-1of1.tar')
# my_tar.extractall('/Users/sangdi/tar') # specify which folder to extract to
# my_tar.close()

# states_provinces = cartopy.feature.NaturalEarthFeature(
#         category='cultural',
#         name='admin_1_states_provinces_lines',
#         scale='10m',
#         facecolor='none')

#np.seterr(all='ignore')

l1bfiles = sorted(glob.glob('/Users/sangdi/1511892-1of1/W_XX-EUMETSAT-Darmstadt,VIS+IR+HRV+IMAGERY,MSG1+SEVIRI_C_EUMG_20190405000009.nc'))
#l1bfiles = sorted(glob.glob('rawData/SEVIRI/*.nc'))



for ifile,file in enumerate(l1bfiles):
    filename = os.path.basename(file)
    time = datetime.datetime.strptime(filename.split('_')[4],'%Y%m%d%H%M%S.nc')
    scn = Scene(reader='seviri_l1b_nc', filenames=[file])    
    scn.load(['dust'])
    q = scn['dust'].attrs['start_time']  #access time of the data
    ### q = scn['dust'].max().compute()   ##compute the maximum
    p = scn['dust'].coords['bands']
    # # extract the lon lat info
 


    # lons, lats = scn['dust'].attrs['area'].get_lonlats()

    # plot with satpay
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
    plt.savefig(fname="/Users/sangdi/test/SEVIRI_{:s}.png".format(time.strftime('%Y%m%d%H%M%S')),dpi=800, bbox_inches='tight')
    # scn.save_datasets(filename="/Users/sangdi/tar/SEVIRI_{:s}.png".format(time.strftime('%Y%m%d%H%M%S')),writer='simple_image')


images = []
filenames = sorted(glob.glob('/Users/sangdi/1511892-1of1/SEVIRI_2019*.png'))
print(filenames)
for filename in filenames:
    images.append(imageio.imread(filename))
imageio.mimsave('/Users/sangdi/1511892-1of1/carin.gif',images,duration=0.5)
# zzoptimize('seviri/RGB.gif') # For overwriting the original one






# ax.gridlines()

# gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=1, color='gray', alpha=0.5, linestyle='--')
# #
# # gl.xlocator = mticker.FixedLocator([-155.9,-154.8, -153.6,-152.4,-151.2,-150])
# # gl.ylocator = mticker.FixedLocator([58,57.5, 57,56.5,56.5,56,55.5,55])
# # gl.ylabels_right = False
# # gl.xlabels_bottom = None
# gl.xformatter = LONGITUDE_FORMATTER
# gl.yformatter = LATITUDE_FORMATTER
# gl.ylabel_style = {'size': 13,'color': 'black'}
# gl.xlabel_style = {'size': 13,'color': 'black'}

# crs = scn['dust'].attrs['area'].to_cartopy_crs()
# plt.figure()
# ax = plt.axes(projection = crs)

# my_data = scn['dust']
# my_data.plot.imshow(transform=crs)
# ax.coastlines()
# ax.gridlines()

# scn.save_datasets(filename="/Users/sangdi/SEVIRI_{:s}.png".format(time.strftime('%Y%m%d%H%M%S')),writer='simple_image')   

# plt.show()
# plt.savefig("test.png", dpi=500)
