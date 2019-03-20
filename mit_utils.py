# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 23:47:38 2019

@author: Winham

辅助函数
"""

import warnings
import numpy as np
from scipy.signal import resample
import pywt
from sklearn.preprocessing import scale
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.utils.multiclass import unique_labels
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")


def sig_wt_filt(sig):
    """
    对信号进行小波变换滤波
    :param sig: 输入信号，1-d array
    :return: 小波滤波后的信号，1-d array

    """
    coeffs = pywt.wavedec(sig, 'db6', level=9)
    coeffs[-1] = np.zeros(len(coeffs[-1]))
    coeffs[-2] = np.zeros(len(coeffs[-2]))
    coeffs[0] = np.zeros(len(coeffs[0]))
    sig_filt = pywt.waverec(coeffs, 'db6')
    return sig_filt


def multi_prep(sig, target_point_num=1280):
    """
    信号预处理
    :param sig: 原始信号，1-d array
    :param target_point_num: 信号目标长度，int
    :return: 重采样并z-score标准化后的信号，1-d array
    """
    assert len(sig.shape) == 2, 'Not for 1-D data.Use 2-D data.'
    sig = resample(sig, target_point_num, axis=1)
    for i in range(sig.shape[0]):
        sig[i] = sig_wt_filt(sig[i])
    sig = scale(sig, axis=1)
    return sig


def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues):
    """
    绘制混淆矩阵图，来源：
    https://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html#sphx-glr-auto-examples-model-selection-plot-confusion-matrix-py
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    cm = confusion_matrix(y_true, y_pred)
    classes = classes[unique_labels(y_true, y_pred)]
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax


def print_results(y_true, y_pred, target_names):
    """
    打印相关结果
    :param y_true: 期望输出，1-d array
    :param y_pred: 实际输出，1-d array
    :param target_names: 各类别名称
    :return: 打印结果
    """
    overall_accuracy = accuracy_score(y_true, y_pred)
    print('\n----- overall_accuracy: {0:f} -----'.format(overall_accuracy))
    cm = confusion_matrix(y_true, y_pred)
    for i in range(len(target_names)):
        print(target_names[i] + ':')
        Se = cm[i][i]/np.sum(cm[i])
        Pp = cm[i][i]/np.sum(cm[:, i])
        print('  Se = ' + str(Se))
        print('  P+ = ' + str(Pp))
    print('--------------------------------------')
