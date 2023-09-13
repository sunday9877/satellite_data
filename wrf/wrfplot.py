#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 19 12:28:36 2022

@author: sangdi
"""

from matplotlib import cm,colors
import matplotlib.pyplot as plt
import numpy as np
import netCDF4 as nc
import math
import matplotlib as mpl
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

path ="/data/disang/WRF/Build_WRF/WRF/test/em_real/"
pdir ="/data/disang/WRF/data/pic/"

filelist = glob.glob(os.path.join(path,'wrfout_d01_2018-05*'))

for file in filelist:
    filename = os.path.basename(file)
    time = datetime.datetime.strptime(filename.split('d01_')[1],'%Y-%m-%d_%H:%M:%S')
    # orbit = filename.split('-')[3][0:6]
    


    with Dataset(file, mode='r') as fh:
        
        hz = 21 ###height level

        # dbz  = data.variables["COMPOSITE_REFL_10CM"][ti[i],xs:xe,ys:ye]
        lat  = fh.variables["XLAT"][0,:,:]
        lon  = fh.variables["XLONG"][0,:,:]
        u  = fh.variables["U"][0,hz,:,0:269]
        v  = fh.variables["V"][0,hz,0:249,:] 

        ## U and V are not defined at the center of a cell, but at east-west and north-south faces.
        ## Dimension of U is 1 larger than the number of cells in x-direction.
        ## Dimension of V is 1 larger than the number of cells in y-direction.

        ws = np.sqrt(u**2 + v**2) 

        lo = lon.flatten()
        la = lat.flatten()
        ws1= ws.flatten()
        
        ## figure plot
        fig = plt.figure(figsize=(12,7))

        cmap1 = mpl.cm.turbo

        ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax.set_extent([40, 90, 30, 60], crs=ccrs.PlateCarree())
        # ax.set_extent([48, 63, 42.5, 49], crs=ccrs.PlateCarree())
        # ax.set_extent([48, 56, 40, 48], crs=ccrs.PlateCarree())



        ### plot the map
        im = ax.tricontourf(lo,la,ws1,shading='flat', cmap=cmap1,transform=ccrs.PlateCarree())


        ax.add_feature(cfeature.COASTLINE.with_scale('10m'),linewidth=.7,edgecolor='k',alpha=.5,zorder=100)
        # ax.add_feature(states_provinces,linewidth=.3,linestyle='--',edgecolor='k',alpha=.5,zorder=100)
        ax.add_feature(cfeature.LAKES.with_scale('10m'),linewidth=.7,facecolor='none',edgecolor='k',alpha=.5,zorder=100)
        ax.add_feature(cfeature.BORDERS.with_scale('10m'),color='blue',linewidth=1,linestyle='--',edgecolor='k',alpha=.5,zorder=100)
        ax.set_title('Windspeed'+str(time),fontsize=14)

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
        cb3.set_label('wind speed')

        fig.savefig(pdir+'Windspeed'+str(time)+'.png',bbox_inches="tight",dpi=600)
        plt.close(fig)
        
