#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 02:07:34 2017

@author: gaokuang
"""
import matplotlib  
matplotlib.use('Agg') 
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

data=sio.loadmat('testingDataFusion.mat')
data=data['outputData']
data=np.where(data>=15,1,0)
data=data.reshape(90,548,421)

London=[142,328]
cityX=[84,199,140,236,315,358,363,423,125,189]
cityY=[203,371,234,241,281,207,237,266,375,274]
day=1
hour=3-1


for i in range(90):
    if i == 0:
        p = plt.imshow(data[i].transpose(),cmap=cm.Blues)
        plt.xlabel('X axis')
        plt.ylabel('Y axis')
        fig = plt.gcf()
        ax = plt.gca()
        ax.xaxis.set_ticks_position('top')
        ax.yaxis.set_ticks_position('left')
        plt.clim()   # clamp the color limits
        hour=hour+1
        
    else:
        p.set_data(data[i].transpose())
        hour=hour+1

    for k in range(10):    
        plt.text(cityX[k],cityY[k],str(k+1),color='r')
    plt.scatter(London[0],London[1],c='y',marker='x')
    fig.suptitle('day:'+str(day)+',hour:'+str(hour), fontsize=14, fontweight='bold')
    print("step", i)
#    plt.pause(0.5)
    plt.savefig('p'+str(i)+'.png')
    if hour==20:
        hour=3-1
        day=day+1
    