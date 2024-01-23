# -*- coding = utf-8 -*-
# @Time : 2023/4/26 12:56
# @Author : Lowry
# @File : data
# @Software : PyCharm

import os
import numpy as np


def get_bits(max_feature_length=10000, path=None):
    """
    Get seeds' bits

    :param max_feature_length:
    :param path: seed path
    :return: data of seeds' bits
    """
    x_data = []
    ll = 0
    with open(path, "r", encoding='iso-8859-1') as f:
        t = f.read()
        byarray = bytearray(t, encoding='iso-8859-1')
        ll += len(byarray)
        longest_testcase_length = 0
        if len(byarray) > longest_testcase_length:
            longest_testcase_length = len(byarray)
        if len(byarray) > max_feature_length:
            byarray = byarray[:max_feature_length]
        else:
            byarray += (max_feature_length - len(byarray)) * b'\x00'
        b16_list = [hex(x) for x in byarray]
        b10_list = []
        for i in b16_list:
            b10 = int(i, 16)
            b10_list.append(b10)
        x_data.append(b10_list)
    return x_data[0], ll


def get_byte(dir_path=None):
    """
    Get seeds' bytes sequences
    :param dir_path: seed path
    """
    X = []  # Used to store feature values
    X_file_name = []    # Used to store the selected seed file name
    file_len = []       # Used to store the length of seed bytes
    files = os.listdir(dir_path)
    for file in files:
        if file == '.state':
            continue
        X_file_name.append(file)  # Store all seed file names
        file = dir_path + '' + file
        x_data, x_len = get_bits(path=file)
        X.append(x_data)
        file_len.append(x_len)
    X = np.array(X)
    return X, X_file_name, file_len
