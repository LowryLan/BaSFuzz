# -*- codeing = utf-8 -*-
# @Time : 2023/7/12 8:16
# @Author : Lowry
# @File : similarity
# @Software : PyCharm

import numpy as np
import random
from tqdm import trange, tqdm


def sim_a(byte_array=None, seed_list=None, max_len=None):
    """
    计算相似度度量a

    :parameter byte_array: 字节序列
    :parameter seed_list: 种子名序列
    :parameter max_len: 字节序列最大长度

    :return similarity_a_list: 相似度度量a结果
    """
    similarity_a_list = []
    byte_list = byte_array.tolist()
    seed_num = len(seed_list)

    for i in tqdm(range(len(byte_list)), desc='Similarity_a'):
        similarity_a = []
        for j in range(max_len):
            byte_row = byte_array[:, j].tolist()
            num = byte_row.count(byte_list[i][j])
            sim = round(num / seed_num, 6)
            similarity_a.append(sim)
        similarity_a_list.append(round(sum(similarity_a), 6))
    return similarity_a_list


def sim_b(byte_array=None, seed_list=None, max_len=None):
    """
    计算相似度度量b

    :parameter byte_array: 字节序列
    :parameter seed_list: 种子名序列
    :parameter max_len: 字节序列最大长度

    :return similarity_b_list: 相似度度量b结果
    """
    similarity_b_list = []
    similarity_b_matrix = []                        # 类上三角矩阵，每个元素记录第i、j种子的相似度
    byte_list = byte_array.tolist()
    seed_num = len(seed_list)

    for i in range(seed_num):
        similarity_b = []
        for q in range(i):                          # 填充下三角元素，减少逐个遍历的时间
            similarity_b.append(similarity_b_matrix[q][i])
        similarity_b.append(1)
        for j in tqdm(range(seed_num-i-1), desc=f'Similarity_b({i+1}/{seed_num})--->seed {seed_list[i][:9]}'):
            j += (i + 1)
            similarity_num = 0                      # 相同位置字节大小相同的数量
            for t in range(max_len):
                if byte_list[i][t] == byte_array[j][t]:
                    similarity_num += 1
            similarity_b.append(round(similarity_num/max_len, 6))       # 第i、j种子所有同一位置字节相同的比例
        similarity_b_matrix.append(similarity_b)                        # 更新矩阵
        similarity_b_list.append(round(sum(similarity_b), 6))           # 填充第i个种子的相似度度量b
    return similarity_b_list


def similarity(byte_array=None, seed_list=None, max_len=None):
    """
    计算自适应相似度similarity

    :parameter byte_array: 字节序列
    :parameter seed_list: 种子名序列
    :parameter max_len: 字节序列最大长度

    :return similarity_list: 相似度度量结果
    """
    a_list = sim_a(byte_array=byte_array, seed_list=seed_list, max_len=max_len)
    b_list = sim_b(byte_array=byte_array, seed_list=seed_list, max_len=max_len)

    k = 0.7
    # 超参数k(α)

    similarity_list = [round(a_list[i] * k + b_list[i] * (1 - k), 6) for i in range(len(seed_list))]
    return similarity_list


def get_index(ele=None, list_src=None):
    """

    :param ele: 指定元素
    :param list_src: 列表

    :return index_list: 该元素存在于列表中的索引
    """
    index_list = []
    for i in range(len(list_src)):
        if list_src[i] == ele:
            index_list.append(i)
    return index_list


def order_seed(similarity_list=None, seed_list=None):
    """
    根据similarity从大到小对种子进行排序

    :param similarity_list: 自适应相似度序列
    :param seed_list: 种子名序列

    :return seed_list_new: 排序结果
    """
    seed_list_new = []
    similarity_sort = sorted(similarity_list)
    i = 0
    temp = 0                            # 记录当前相似度得分
    while i < len(seed_list):
        sim = similarity_sort[i]
        if sim == temp:
            i += 1
            continue
        else:
            temp = sim
            index_list = get_index(sim, similarity_list)
            for j in index_list:
                seed_list_new.append(seed_list[j])
            i += 1
    return seed_list_new


def similarity_re(byte_array=None, seed_list=None, max_len=None):
    """
    主函数

    :parameter byte_array: 字节序列
    :parameter seed_list: 种子名序列
    :parameter max_len: 字节序列最大长度

    :return similarity_list: 相似度度量结果
    """

    """ 计算相似度 """
    similarity_list = similarity(byte_array=byte_array, seed_list=seed_list, max_len=max_len)

    """ 排序 """
    seed_list_new = order_seed(similarity_list=similarity_list, seed_list=seed_list)

    """ 选择低质量种子（对比实验内容） """
    # seed_list_new = choose_bad_seed(seed_list_new)
    # print(len(seed_list_new))
    # print("============")
    # for i in seed_list_new:
    #     print(i)

    return seed_list_new


def order_by_id(seed_list):
    """
    根据种子id排序

    :param seed_list: 种子名序列
    :return: 顺序种子队列
    """
    seed_list_new = []
    id_list = [int(i[3:9]) for i in seed_list]
    id_order = sorted(id_list)
    for j in range(len(id_list)):
        seed_id = id_order[j]
        index = id_list.index(seed_id)
        seed_name = seed_list[index]
        seed_list_new.append(seed_name)
    return seed_list_new


def choose_bad_seed(seed_list):
    """
    选择低质量种子

    :param seed_list:
    :return: 低质量种子队列
    """
    seed_list = seed_list[int(len(seed_list) / 2):]
    seed_list_new = order_by_id(seed_list)
    return seed_list_new


def test():
    byte_list = []
    seed_list = []
    for i in tqdm(range(100), desc='Initial seed'):
        seed = 'id:' + str(i)
        byte = [random.randint(0, 255)for j in range(10000)]
        byte_list.append(byte)
        seed_list.append(seed)
    byte_array = np.array(byte_list)
    similarity_re(byte_array=byte_array, seed_list=seed_list, max_len=10000)
    print('finish')


# test()
