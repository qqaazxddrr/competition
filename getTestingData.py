#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 12:21:48 2017

@author: gaokuang
"""

import csv
import scipy.io as sio
import numpy as np

testingData=[]
RMSE=np.array([2.3452473930597999, 2.4057958282882739, 2.3378241868084735, 2.5266803221778158, 2.3765816290891069, 2.4230948602694733, 2.3681212512848147, 2.4593013541798214, 2.5012042761101116, 2.4184522510987279])
coeff=RMSE/np.sum(RMSE)
coeff=coeff.tolist()
i=-1
tempData=0
outputData=[]



with open('ForecastDataforTesting_20171124.csv', "r") as f:
    lines = csv.reader(f)
    for line in lines: 
        i=i+1
        if i>0:
            if i%10==0:
                tempData=tempData+float(line[5])*coeff[9]
                outputData.append(tempData)
                tempData=0    
            else:
                tempData=tempData+float(line[5])*coeff[int(i%10-1)]
                
sio.savemat('testingDataFusion.mat', {'outputData': outputData})
                
                
            
           
        
            

        

