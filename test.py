# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 23:27:28 2019

@author: Winham

网络测试
"""

import os
import numpy as np
from keras.models import load_model
from keras.utils import to_categorical
import mit_utils as utils
import time
import matplotlib.pyplot as plt

os.environ["TF_CPP_MIN_LOG_LEVEL"] = '2'
data_path = 'E:/MIT_Scheme/Data_npy/'

test_data = {'N': 'N_SEG_test.npy',
             'V': 'VEB_SEG_test.npy',
             'S': 'SVEB_SEG_test.npy',
             'F': 'F_SEG_test.npy',
             'Q': 'Q_SEG_test.npy'}

target_class = ['N', 'V', 'S', 'F', 'Q']
target_sig_length = 1280
tic = time.time()
for i in range(len(target_class)):
    TestXt = np.load(data_path + test_data[target_class[i]])
    TestYt = np.array([i]*TestXt.shape[0])
    if i == 0:
        TestX = utils.multi_prep(TestXt, target_sig_length)
        TestY = TestYt
    else:
        TestX = np.concatenate((TestX,
                                utils.multi_prep(TestXt, target_sig_length)))
        TestY = np.concatenate((TestY, TestYt))

TestX = np.expand_dims(TestX, axis=2)
TestY = to_categorical(TestY, num_classes=len(target_class))
toc = time.time()

del TestXt, TestYt

print('Time for data processing--- '+str(toc-tic)+' seconds---')
model_name = 'myNet.h5'
model = load_model(model_name)
model.summary()
pred_vt = model.predict(TestX, batch_size=128, verbose=1)
del TestX
pred_v = np.argmax(pred_vt, axis=1)
true_v = np.argmax(TestY, axis=1)

utils.plot_confusion_matrix(true_v, pred_v, np.array(target_class))
utils.print_results(true_v, pred_v, target_class)
plt.show()
