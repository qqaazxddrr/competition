#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 00:35:54 2017

@author: gaokuang
"""

import scipy.io as sio
import numpy as np
import progressbar

def sortModel(model):
    print('Sorting data...\n')
    model = np.core.records.fromarrays(model.transpose(), 
                                             names='x,y,d,h,m,w',
                                             formats = 'int,int,int,int,int,float')
    model=np.sort(model,order=['d','h','x','y'])
    return model

#def searchModelWind(model,gt_pattern):
#    wind=0
#    a=model[:,0:4]
#    b=gt_pattern
#    model_index=np.where(np.sum(a==b,1)==4)
#    wind=model[model_index,5]
#    return wind


data=sio.loadmat('gTruth.mat')
gTruth=data['gtruth']
SE_sum=0  #需要注意每次迭代后归零
index=0   #需要注意每次迭代后归零
RMSE=[]


for i in range(1,11):
    p = progressbar.ProgressBar()
    data=sio.loadmat('model'+str(i)+'.mat')
    print('Loading data '+str(i)+'...\n')
    model=data['model'+str(i)]
    model=sortModel(model)

 
    row,col=gTruth.shape

    for j in p(range(row)):       
        gt_wind=gTruth[j][4]
        model_wind=model['w'][j]
        SE=(model_wind-gt_wind)**2
        SE_sum=SE_sum+SE
        index=index+1
    RMSE.append(np.sqrt(SE_sum/index))
    SE_sum=0
    index=0
print('RMSE Result:\n')
print(RMSE)
        
    
