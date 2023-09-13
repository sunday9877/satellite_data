

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 13:56:39 2022

@author: sangdi
"""

import numpy as np
import glob
import datetime
import os
from netCDF4 import Dataset



path ="/nobackup/dsang1/wrfnew/Build_WRF/WRF/test/em_real/"
pdir ="/nobackup/dsang1/wrfnew/Build_WRF/WRF/test/em_real/nctro/"

filelist = glob.glob(os.path.join(path,'wrfout_d01_2018-05*'))

l1 = len(filelist)
n = -1
toutput_a1 = np.zeros((l1,669,542), dtype=np.float32)


for file in filelist:
    filename = os.path.basename(file)
    time = datetime.datetime.strptime(filename.split('d01_')[1],'%Y-%m-%d_%H:%M:%S')
    # orbit = filename.split('-')[3][0:6]
    n = n + 1
    print(str(n))


    with Dataset(file, mode='r') as ncfile:


        # Extract the pressure, geopotential height, and wind variables
        lats  = ncfile["XLAT"][0,:,:]
        lons  = ncfile["XLONG"][0,:,:]


        # Extract the totedust emisssion
        d1 =ncfile["TOT_EDUST"][0,:,:]
        ws=d1.copy()
        ws[ws==0]=np.nan
        tde = ws

        # Extract the p10,p25

        p10 =ncfile["PM10"][0,0,:,:]
        p25 =ncfile["PM2_5_DRY"][0,0,:,:]

        # Extract the AOD

        ph  = ncfile.variables["PH"][0,:,:,:]
        phb  = ncfile.variables["PHB"][0,:,:,:]
        ht = ncfile.variables["HGT"][0,:,:]
        e1 = ncfile.variables["EXTCOF55"][0,:,:,:]

        ### geopotential height
        th = (ph+phb)/9.81
        ### layer thickness
        dth = np.diff(th,axis = 0)
        
        ### AOD
        ao = dth * e1
        aod = np.sum(ao, axis=0)
        aod = aod/1000
        
        
        
        
        ### dep ug/m2/s
        e1 =ncfile["DRYDEP_1"][0,:,:]
        e2 =ncfile["DRYDEP_2"][0,:,:]
        e3 =ncfile["DRYDEP_3"][0,:,:]
        e4 =ncfile["DRYDEP_4"][0,:,:]
        e5 =ncfile["DRYDEP_5"][0,:,:]
        
        
        
                # total dry deposition
        d1 = e1+e2+e3+e4+e5
        ws=d1.copy()
        ws = 0-ws
        
        tm = ws*3600*4000*4000
        
        ### tm in kg every cell each time atep
        
        tm = tm/1000000000
         #### gravitational settling
        eg1 =ncfile["GRASET_1"][0,:,:]
        eg2 =ncfile["GRASET_2"][0,:,:]
        eg3 =ncfile["GRASET_3"][0,:,:]
        eg4 =ncfile["GRASET_4"][0,:,:]
        eg5 =ncfile["GRASET_5"][0,:,:]
        
        g1 = eg1+eg2+eg3+eg4+eg5
        
        
        # print(mas)
        
        ###ncfile save
        ncfile = Dataset(pdir + 'AFWA2'+str(time)+'.nc',mode='w',format='NETCDF4')
        
        
        # ### Define two variables with the same names as dimensions
        x_dim = ncfile.createDimension('xd', 542)     # latitude axis
        y_dim = ncfile.createDimension('yd', 669)

        ### create variables, dim var must have ',' at the end of it for lon, lat
        lat = ncfile.createVariable('lat', np.float32, ('xd','yd'))
        lat.long_name = 'latitude'
        lon = ncfile.createVariable('lon', np.float32, ('xd','yd'))
        lon.long_name = 'longitude'
        FR = ncfile.createVariable('tdep',np.float64,('xd','yd'))
        FR.long_name = 'total deposition'
        FR.units ='kg m^-2'
        TDM = ncfile.createVariable('tde',np.float64,('xd','yd'))
        TDM.long_name = 'total emission'
        TDM.units ='kg m^-2'
        P10 = ncfile.createVariable('p10',np.float64,('xd','yd'))
        P10.long_name = 'PM10'
        P10.units ='ug m^-3'
        P25 = ncfile.createVariable('p25',np.float64,('xd','yd'))
        P25.long_name = 'PM2.5'
        P25.units ='ug m^-3'
        AOD = ncfile.createVariable('aod',np.float64,('xd','yd'))
        AOD.long_name = 'Aerosol Optical Depth'
        G1 = ncfile.createVariable('gra',np.float64,('xd','yd'))
        G1.long_name = 'Accumulated dust gravitational settling'
        G1.units ='kg m^-2'
        
        
        ###pass value to the variables
        lon[:,:] = lons #The "[:]" at the end of the variable instance is necessary
        lat[:,:] = lats
        FR[:,:] = tm
        TDM[:,:] = tde
        P10[:,:] = p10
        P25[:,:] = p25
        AOD[:,:] = aod
        G1[:,:] = g1
        
        ncfile.close()
                                
        
        
