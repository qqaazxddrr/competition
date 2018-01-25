#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 18:20:30 2017

@author: gaokuang
"""

import pandas as pd
import numpy as np
from datetime import *
import csv
from AStar import findPath
import scipy.io as sio

# simple submit
def simSub(sXid,sYid,eXid,eYid,target,date,pic):
    #### create one submit path
    
    sub_df = pd.DataFrame(columns=['target','date','time','xid','yid'])
    sub=np.array(findPath((sXid,sYid),(eXid,eYid),pic))
    sub_df['xid'] = sub[:,0]
    sub_df['yid'] = sub[:,1]
    sub_df.xid = sub_df.xid.astype(np.int32)
    sub_df.yid = sub_df.yid.astype(np.int32)
    sub_df.target = target
    sub_df.date = date
    #### add time
    ti = datetime(2017,11,21,3,0)
    tm = [ti.strftime('%H:%M')]
    for i in range(len(sub)-1):
        ti = ti + timedelta(minutes=2)
        tm.append(ti.strftime('%H:%M'))
    sub_df.time = tm
    return sub_df

#def submit_phase():
#    city = pd.read_csv('CityData.csv')
#    city_array = city.values
#    sub_csv = pd.DataFrame(columns=['target','date','time','xid','yid'])
#    for date in range(5):
#        for tar in range(10):
#            sub_df = simSub(city_array[0][1],city_array[0][2],\
#                            city_array[tar+1][1],city_array[tar+1][2],\
#                            tar+1,date+6)
#            sub_csv=pd.concat([sub_csv,sub_df],axis=0)
#    sub_csv.target = sub_csv.target.astype(np.int32)
#    sub_csv.date = sub_csv.date.astype(np.int32)
#    sub_csv.xid = sub_csv.xid.astype(np.int32)
#    sub_csv.yid = sub_csv.yid.astype(np.int32)
#    with open('output.csv', 'wb') as f:
#    writer = csv.writer(f)
#    for row in sub_csv:
#        writer.writerow(row)

def submit(London,goal,target,data,pic):
    sub_csv = pd.DataFrame(columns=['target','date','time','xid','yid'])
    sub_df = simSub(London[0],London[1],goal[0],goal[1],target,data+5,pic)
    sub_csv=pd.concat([sub_csv,sub_df],axis=0)
    sub_csv.target = sub_csv.target.astype(np.int32)
    sub_csv.date = sub_csv.date.astype(np.int32)
    sub_csv.xid = sub_csv.xid.astype(np.int32)
    sub_csv.yid = sub_csv.yid.astype(np.int32)
    with open('data'+str(data+5)+'_city_'+str(target)+'.csv', 'wb') as f:
        writer = csv.writer(f)
        for row in sub_csv.values:
            writer.writerow(row)
    return sub_csv

if __name__ == "__main__": 
    London=[142,328]
    goal=[199,371]
    data=sio.loadmat('testingDataFusion.mat')
    data=data['outputData']
    data=np.where(data>=15,1,0)
    data=data.reshape(90,548,421)
    a=submit(London,goal,2,10,data[72])
        