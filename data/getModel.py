#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 00:50:24 2017

@author: gaokuang
"""
import csv
import scipy.io as sio
import numpy as np
import getopt
import sys

i=0
modelL=[]

try:
    opts, args = getopt.getopt(sys.argv[1:],"hm:",["modelNumber="])
except getopt.GetoptError:
    print ('test.py -m <modelNumber>')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print ('test.py -m <modelNumber>')
        sys.exit()
    elif opt in ("-m", "--modelNumber"):
        modelNum = arg


with open('ForecastDataforTraining_20171124.csv', "r") as f:
    lines = csv.reader(f)
    for line in lines: 
        if line[4]==str(modelNum):
            modelL.extend(list(map(eval,line)))
            i=i+1

model=np.array(modelL).reshape(int(i),6)

sio.savemat('model'+modelNum+'.mat', {'model'+modelNum: model})
    