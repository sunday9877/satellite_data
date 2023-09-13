#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 20 15:26:14 2021

@author: sangdi
"""

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
import imageio
from pygifsicle import optimize

    # # Directory
directory2 = 'fig'
directory1 = 'natf'


### create new directory
# # Parent Directory path
parent_dir = "/data/disang/seviri/2018/m01/180101/"
  
# # Path
path1 = os.path.join(parent_dir, directory1)
# os.mkdir(path1)
path2 = os.path.join(parent_dir, directory2)
# os.mkdir(path2)



images = []
filenames = sorted(glob.glob(path2 + '/SEVIRI*.png'))
#print(filenames)
for filename in filenames:
    images.append(imageio.imread(filename))
imageio.mimsave('/SEVIRI_180101.gif' ,images,duration=0.5)
optimize('/SEVIRI_180101.gif')

                