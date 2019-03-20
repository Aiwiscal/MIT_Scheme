# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 10:29:47 2019

@author: Winham

网络配置

"""


class Config(object):
    def __init__(self):
        self.conv_subsample_lengths = [1, 2, 1, 2, 1, 2, 1, 2]
        self.conv_filter_length = 32
        self.conv_num_filters_start = 12
        self.conv_init = "he_normal"
        self.conv_activation = "relu"
        self.conv_dropout = 0.5
        self.conv_num_skip = 2
        self.conv_increase_channels_at = 2
        self.batch_size = 128
        self.input_shape = [1280, 1]
        self.num_categories = 5

    @staticmethod
    def lr_schedule(epoch):
        lr = 0.1
        if epoch >= 20 and epoch < 40:
            lr = 0.01
        if epoch >= 40:
            lr = 0.001
        print('Learning rate: ', lr)
        return lr
