# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 13:16:05 2019

@author: Winham

mat文件转为npy文件

"""

import os
import numpy as np
import scipy.io as sio

mat_path = 'E:/MIT_Scheme/Data_mat/'
npy_path = 'E:/MIT_Scheme/Data_npy/'

mat_files = os.listdir(mat_path)

for i in range(len(mat_files)):
    file_name = mat_files[i]
    if file_name.endswith('train.mat'):
        key_name = file_name[:-10]
        func = 'train'
    else:
        key_name = file_name[:-9]
        func = 'test'
    sig = sio.loadmat(mat_path+file_name)[key_name]
    np.save(npy_path+key_name+'_'+func+'.npy', sig)
