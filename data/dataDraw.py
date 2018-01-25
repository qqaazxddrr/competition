#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 18:07:44 2017

@author: gaokuang
"""
import matplotlib  
#matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
from matplotlib import cm

data=sio.loadmat('gTruth.mat')
model1=data['gtruth']
Z_All=model1[:,4]
#Z_All[Z_All<15]=0
#Z_All[Z_All>=15]=1
Z_All=np.where(Z_All>=15,1,0)
#Z_All=Z_All.reshape(int(20763720/(421*548)),421,548)
Z_All=Z_All.reshape(int(20763720/(421*548)),548,421)

x = np.arange(548)
y = np.arange(421)



for i in range(90):
    if i == 0:
        p = plt.imshow(Z_All[i].transpose(),cmap=cm.Blues)
        plt.xlabel('X axis')
        plt.ylabel('Y axis')
        fig = plt.gcf()
        ax = plt.gca()
        ax.xaxis.set_ticks_position('top')
        ax.yaxis.set_ticks_position('left')
        plt.clim()   # clamp the color limits
        
    else:
        p.set_data(Z_All[i])
        plt.pause(0.2)

    print("step", i)
#    w