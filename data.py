# -*- coding = utf-8 -*-
# @Time : 2023/4/26 12:56
# @Author : Lowry
# @File : test
# @Software : PyCharm
import os
import numpy as np


def get_edge_cov(file_path=None):
    """
    获取边覆盖情况
    :param file_path: 边覆盖信息文件路径
    :return edge_list: 边覆盖结果，存有边号的列表
    """
    edge_list = []  # 边覆盖结果
    """ 读取边覆盖信息文件 """
    f = open(file_path, "r", encoding='utf-8')
    line = f.readline()  # 读取第一行
    i = 1
    while line:
        edge_cov = line.split(',')
        i += 1
        """ 将覆盖边的位置存入 edge_list """
        edge_list.append(int(t) for t in edge_cov[:-2])  # 列表增加
        line = f.readline()  # 读取下一行
    print(edge_list)
    f.close()
    array_e = np.ones((len(edge_list), 65536)) * 0
    for i in range(len(edge_list)):
        print(edge_list[i])
        for j in edge_list[i]:
            array_e[i, j] = 1
    edge_array = np.array(edge_list)
    array_e = np.delete(array_e, np.where(~array_e.any(axis=0))[0], axis=1)
    print(array_e)
    return edge_array


def get_bits(max_feature_length=10000, path=None):
    """
    读取种子文件内容为二进制数据
    :param max_feature_length:
    :param path: 种子路径
    :return: 二进制数据
    """
    x_data = []
    ll = 0
    with open(path, "r", encoding='iso-8859-1') as f:
        t = f.read()
        byarray = bytearray(t, encoding='iso-8859-1')
        ll = ll + len(byarray)
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
    获取种子字节序列
    :param dir_path: 种子目录路径
    """
    X = []  # 用于存储特征值
    X_file_name = []    # 用于存储被选出的种子文件名
    file_len = []       # 用于存储种子字节的长度
    files = os.listdir(dir_path)
    for file in files:  # 遍历文件夹
        if file == '.state':
            continue
        X_file_name.append(file)  # 存储所有种子文件名
        file = dir_path + '' + file
        x_data, x_len = get_bits(path=file)
        X.append(x_data)
        file_len.append(x_len)
    X = np.array(X)
    return X, X_file_name, file_len


def test():
    str = "qwertyuiop[]asdfghjkl;'zxcvbnm,./\!@#$%^&*()_+-=`~"
    print(type(str))
    byarray = bytearray(str, encoding='iso-8859-1')
    byarray += (100 - len(byarray)) * b'\x00'

    b16_list = [hex(x) for x in byarray]
    print(byarray)
    b10_list = []
    for i in b16_list:
        b10 = int(i, 16)
        b10_list.append(b10)
    print(b10_list)
