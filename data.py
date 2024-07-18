# -*- coding = utf-8 -*-
# @Time : 2023/4/26 12:56
# @Author : Lowry
# @File : data
# @Software : PyCharm

import os
import numpy as np


def get_bits(max_feature_length, path=None):
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


def get_max_file_len(dir_path=None):
    largest_file_size = 0
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            if file_size > largest_file_size:
                largest_file_size = file_size
    return largest_file_size


def get_byte(dir_path=None):
    """
    Get seeds' bytes sequences
    :param dir_path: seed path
    :param max_len: max length
    """
    X = []  # Used to store feature values
    X_file_name = []    # Used to store the selected seed file name
    file_len = []       # Used to store the length of seed bytes
    files = os.listdir(dir_path)
    max_len = get_max_file_len(dir_path=dir_path)
    if max_len > 10000:
        max_len = 10000
    print("The maximum length of the seed：" + str(max_len))
    for file in files:
        if file == '.state':
            continue
        X_file_name.append(file)  # Store all seed file names
        file = dir_path + '' + file
        x_data, x_len = get_bits(path=file, max_feature_length=max_len)
        X.append(x_data)
        file_len.append(x_len)
    X = np.array(X)
    return X, X_file_name, file_len
