# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 19:02:12 2023

@author: Ayan
"""

# importing libraries
from pyhdf import SD
import numpy as np
import pandas as pd
# from mpl_toolkits.basemap import Basemap, cm
# import matplotlib.pyplot as plt
import sys
from datetime import date, timedelta

#This uses the file "FILE.txt", containing the list of files, in order to read the files
try:
    fileList = open('Ballygunje3.txt','r')
except:
    print('Did not find a text file containing file names (perhaps name does not match)')
    sys.exit()
    
list = []
for FILE_NAME in fileList:
    FILE_NAME = FILE_NAME.strip()
    FILE_NAME = FILE_NAME.replace(FILE_NAME[0:42],'')
    
    try:
        hdf=SD.SD(FILE_NAME)
    except:
        print('Unable to open file: \n' + FILE_NAME + '\n Skipping...')
        continue
    dataset = hdf.datasets()
    lat = hdf.select('Latitude')
    latitude = lat[:]
    lon = hdf.select('Longitude')
    longitude = lon[:]
    AOD = hdf.select('AOD_550_Dark_Target_Deep_Blue_Combined')
    Final_AOD = AOD
    Year = FILE_NAME[10:14]
    Day_num = FILE_NAME[14:17]
    start_date = date(int(Year), 1, 1)
    res_date = start_date + timedelta(days=int(Day_num) - 1)
    res_date = res_date.strftime("%d-%m-%Y")
    Date = np.full((134,203),res_date) # generate 134x203 matrix with Date
    hr = FILE_NAME[18:20]
    Min = FILE_NAME[20:22]
    Time = hr + ':' + Min
    Time = np.full((134,203),Time)
    
    AOD = np.array(Final_AOD)
    AOD = AOD.ravel()
    Lat = np.array(latitude)
    Lat = Lat.ravel()
    Lon = np.array(longitude)
    Lon = Lon.ravel()
    Date = np.array(Date)
    Date = Date.ravel()
    Time = np.array(Time)
    Time = Time.ravel()
    
    Data = pd.DataFrame()
    Data['Date'] = Date
    Data['Time'] = pd.Series(Time)
    Data['Lat'] = pd.Series(Lat)
    Data['Lon'] = pd.Series(Lon)
    Data['AOD'] = pd.Series(AOD)/1000   
    list.append(Data)


Final_df = pd.concat(list, axis =0, ignore_index=True)
Final_df['AOD'] = Final_df['AOD'].replace([-9.999], value = np.nan)
print(Final_df['AOD'].describe())
Final_df = Final_df.dropna(axis = 0, how= 'any')
Jad_df = Final_df.loc[Final_df['Lon'] >= 88.3183]
Jad_df = Jad_df.loc[Final_df['Lon'] <= 88.4093]
Jad_df = Jad_df.loc[Final_df['Lat'] >= 22.4913]
Jad_df = Jad_df.loc[Final_df['Lat'] <= 22.5823]
print(Jad_df)
Jad_df.to_csv('C:/Users/DELL/OneDrive/Desktop/Ballygunje/Ballygunje.csv',index=False)
