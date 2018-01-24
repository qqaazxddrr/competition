#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 11:11:40 2017

@author: gaokuang
"""

import scipy.io as sio
import numpy as np
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

data=sio.loadmat('gtruth.mat')
gt=data['gtruth']

X=list(range(548))
Y=list(range(421))
temp=gt[0:(548*421)]
Z=temp[:,4].reshape(421,548)

X,Y=np.meshgrid(X, Y)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot a basic wireframe.
ax.plot_wireframe(X, Y, Z,rstride=10, cstride=10)

plt.show()


