# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 23:52:16 2019

@author: Winham

网络训练
"""

import os
import numpy as np
from Config import Config
import net
from keras.utils import to_categorical
from keras.callbacks import ModelCheckpoint, LearningRateScheduler
import mit_utils as utils
import time

os.environ["TF_CPP_MIN_LOG_LEVEL"] = '2'
config = Config()
data_path = 'E:/MIT_Scheme/Data_npy/'

# --------------------- 数据载入和整理 -------------------------------
train_data = {'N': 'N_SEG_train.npy',
              'V': 'VEB_SEG_train.npy',
              'S': 'SVEB_SEG_train.npy',
              'F': 'F_SEG_train.npy',
              'Q': 'Q_SEG_train.npy'}

test_data = {'N': 'N_SEG_test.npy',
             'V': 'VEB_SEG_test.npy',
             'S': 'SVEB_SEG_test.npy',
             'F': 'F_SEG_test.npy',
             'Q': 'Q_SEG_test.npy'}

target_class = ['N', 'V', 'S', 'F', 'Q']
target_sig_length = config.input_shape[0]

if config.num_categories != len(target_class):
    config.num_categories = len(target_class)
tic = time.time()
for i in range(len(target_class)):
    TrainXt = np.load(data_path + train_data[target_class[i]])
    TestXt = np.load(data_path + test_data[target_class[i]])
    TrainYt = np.array([i]*TrainXt.shape[0])
    TestYt = np.array([i]*TestXt.shape[0])
    if i == 0:
        TrainX = utils.multi_prep(TrainXt, target_sig_length)
        TestX = utils.multi_prep(TestXt, target_sig_length)
        TrainY = TrainYt
        TestY = TestYt
    else:
        TrainX = np.concatenate((TrainX,
                                 utils.multi_prep(TrainXt, target_sig_length)))
        TestX = np.concatenate((TestX,
                                utils.multi_prep(TestXt, target_sig_length)))
        TrainY = np.concatenate((TrainY, TrainYt))
        TestY = np.concatenate((TestY, TestYt))

del TrainXt, TestXt, TrainYt, TestYt
TrainX = np.expand_dims(TrainX, axis=2)
TestX = np.expand_dims(TestX, axis=2)
TrainY = to_categorical(TrainY, num_classes=len(target_class))
TestY = to_categorical(TestY, num_classes=len(target_class))
toc = time.time()

print('Time for data processing--- '+str(toc-tic)+' seconds---')

# ------------------------ 网络生成与训练 ----------------------------
model = net.build_network(config)
model.summary()
model_name = 'myNet.h5'
checkpoint = ModelCheckpoint(filepath=model_name,
                             monitor='val_categorical_accuracy', mode='max',
                             save_best_only='True')

lr_scheduler = LearningRateScheduler(config.lr_schedule)
callback_lists = [checkpoint, lr_scheduler]
model.fit(x=TrainX, y=TrainY, batch_size=config.batch_size, epochs=50,
          verbose=1, validation_data=(TestX, TestY), callbacks=callback_lists)

del TrainX, TrainY, TestX, TestY
