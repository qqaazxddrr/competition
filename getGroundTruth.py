#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 13:26:44 2017

@author: gaokuang
"""

import csv
import scipy.io as sio
import numpy as np

i=-1
gtruthL=[]

with open('In-ForecastDataforTesting_20171124.csv', "r") as f:
    lines = csv.reader(f)
    for line in lines: 
        if i>=0:
            gtruthL.extend(list(map(eval,line)))
        i=i+1


model=np.array(gtruthL).reshape(int(i),6)

#sio.savemat('model'+modelNum+'.mat', {'model'+modelNum: model})


sio.savemat('testing.mat', {'test': model})