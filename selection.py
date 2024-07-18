# -*- coding = utf-8 -*-
# @Time : 2023/5/5 8:28
# @Author : Lowry
# @File : selection
# @Software : PyCharm

import os
import data
import numpy as np  # numpy 1.24.3
import similarity

import time


def split_list(byte_arr=None, file_list=None, file_len=None):
    """
    draw seeds with 10000+ bytes
    :parameter byte_arr: byte sequence of seed
    :parameter file_list: seed name list
    :parameter file_len: length of byte sequence

    :return: byte_arr_new, file_list_new, byte_arr_full, file_list_full
    """

    byte_arr_new = []  # byte list with 10000- byte
    file_list_new = []  # seed name with 10000- byte
    file_len_new = []  # length of byte sequence with 10000- byte

    for i in range(len(file_len)):
        if file_len[i] <= 10000:
            byte_arr_new.append(byte_arr[i])
            file_list_new.append(file_list[i])
            file_len_new.append(file_len[i])
    byte_arr_new = np.array(byte_arr_new)
    return byte_arr_new, file_list_new, file_len_new


def selection(path=None, project=None):
    """
    Seed Selection based on byte difference analysis

    :param project: project directory name
    :parameter path: out path

    :return: 1 or -1
    """
    if path is None or project is None:
        return 0

    max_length = 10000
    flag = 0  # 1: the longest length of seed is more than 10000 || 0: shorter than 10000
    byte_arr, file_list, file_len = data.get_byte(path)

    byte_arr0 = byte_arr

    if max(file_len) > max_length:
        byte_arr_new, file_list_new, file_len_new = split_list(byte_arr=byte_arr, file_list=file_list, file_len=file_len)
        flag = 1
        byte_arr0 = byte_arr_new

    # only use seeds with 10000- bytes
    if flag == 1:
        file_list = file_list_new
        file_len = file_len_new

    begin = int(time.time())
    similarity_list = similarity.similarity_re(byte_array=byte_arr0, seed_list=file_list, max_len=max(file_len))
    end = int(time.time())

    print("time costs: " + str(end - begin) + "s")
    # Reorder by file id
    file_len_new = file_len
    file_list_new = file_list

    seed_num = int(len(file_len_new) * 0.5)

    """ This is comparing experimental content, that's BaSFuzz↓. """
    # seed_num = len(similarity_list)

    if write_to_file(file_list=file_list_new, project=project, similarity_list=similarity_list, seed_num=seed_num):
        return 1
    else:
        return -1


def write_to_file(file_list=None,  project=None, similarity_list=None, seed_num=None):
    """
    Write weight metric info to file

    :param file_list: file name list
    :param project: project directory name
    :param similarity_list: file name of selected seeds
    :param seed_num: number of selected seeds
    :return: 1 or -1
    """

    if file_list is None:
        return -1

    with open('./programs/' + project + '/weight_info', 'w') as f:
        for t in range(seed_num):
            temp = similarity_list[t]
            i = file_list.index(temp)
            file_name = 'out/queue/' + file_list[i]
            f.write(file_name + '|' + str(seed_num) + '\n')
    return 1


# print(selection('./programs/readelf/out/queue/', project='readelf'))
