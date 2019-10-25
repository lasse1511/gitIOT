#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 08:30:56 2019

@author: rv
"""

import os
import numpy as np
import pandas as pd

data_folder = 'intformat/'
n_s = 12 # bits_per_sample

files = os.listdir(data_folder)
estimation_file  = data_folder + files[0]
try:
    data = np.genfromtxt(estimation_file, delimiter=',').ravel()
except:
    data = np.load(estimation_file).ravel()
    
size = len(data)*n_s

def NumUniqueRows(data):
    return np.unique(data, axis=0).shape[0]

def EstimateDedupCost(N, U, n_s):
    return EstimateGenDedupCost(N,U,n_s, 0)

def EstimateGenDedupCost(N, K, n_s, l):
    return N*(np.ceil(np.log2(U)) + l) + (n_s-l)*K

eps = 0.01#

c = 0
N_T = len(data)
N = N_T
U = 1

maxsize=2e6
if N_T > maxsize:
    print("SHORTENING")
    data = data[:int(maxsize)]
    N_T = len(data)
    size = N_T*n_s

print("Original size:", size/8)

while U < (1-eps)*N:
    c += 1
    extra = N_T%c
    tmpdata = data
    if extra != 0:
        tmpdata = np.hstack((tmpdata, np.zeros(c-extra)))
    
    tmpdata = tmpdata.reshape(-1, c)
    N = N_T//c
#    U = NumUniqueRows(data)
    U = np.unique(tmpdata, axis=0).shape[0]
    print(U/N, EstimateDedupCost(N, U, c*n_s)/8)
    
print("Let c={}".format(c))

"""
Now we move to estimate the deviation length...
For this we use the unpacked data.
"""

unpacked_file = 'unpacked/' + files[0]

try:
    data = np.genfromtxt(unpacked_file[:-4]+'.csv', delimiter=',').ravel()
except:
    data = np.load(unpacked_file).ravel()
    
data = data[:int(maxsize)]
if extra != 0:
    data = np.vstack((data, np.zeros((c-extra, n_s))))
data = data.reshape(-1, n_s*c)
filedf = pd.DataFrame(data)
corrs = filedf.corr()
var_corr = np.max(np.abs(corrs)-np.eye(len(corrs)), axis=0)
order = np.argsort(np.array(var_corr))[::-1]

data = data[:, order]
old_cost = np.inf

dev_size = 1
try:
    data = data[:,:-dev_size]
except:pass

while dev_size < c*n_s:
    dev_size += 1
    K = NumUniqueRows(data)
    cost = EstimateGenDedupCost(N, K, c*n_s, dev_size)
    print(dev_size, K, cost)
    if cost > old_cost:
        break
    old_cost = cost
    data = data[:,:-1]
dev_size -= 1

if dev_size == 1:
    c = 1
    dev_size = 0
    
print("PARAMETERS ESTIMATED: c={}, devsize={}".format(c, dev_size))
