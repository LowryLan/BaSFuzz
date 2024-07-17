# -*- coding = utf-8 -*-
# @Time : 2023/7/12 8:16
# @Author : Lowry
# @File : similarity
# @Software : PyCharm

from tqdm import trange, tqdm
import numpy as np


def sim_a(byte_array=None, seed_list=None, max_len=None):
    """
    Compute byte similarity

    :parameter byte_array: byte sequences
    :parameter seed_list: list of seed name
    :parameter max_len: max length of byte sequences

    :return similarity_a_list: byte similarity score
    """
    similarity_a_list = []

    # 获取数组的形状
    rows, cols = byte_array.shape

    # 创建一个相同形状的数组用于存储结果
    result = np.zeros_like(byte_array)

    # 对每一列进行统计
    for col in tqdm(range(cols), desc='Similarity_a_1'):
        unique, counts = np.unique(byte_array[:, col], return_counts=True)
        count_dict = dict(zip(unique, counts))
        result[:, col] = [count_dict[val] for val in byte_array[:, col]]

    for i in tqdm(range(rows), desc='Similarity_a_2'):
        similarity_a = result[i, :]
        similarity_a_list.append(round(sum(similarity_a), 6))
    return similarity_a_list


def sim_b(byte_array=None, seed_list=None, max_len=None):
    """
    Compute structure similarity

    :parameter byte_array: byte sequences
    :parameter seed_list: list of seed name
    :parameter max_len: max length of byte sequences

    :return similarity_b_list: structure similarity score
    """
    similarity_b_list = []
    similarity_b_matrix = []                        # Record the similarity of the i-th and jth seeds for each element (Similar to an upper triangular matrix)
    # byte_list = byte_array.tolist()
    seed_num = len(seed_list)

    rows, cols = byte_array.shape

    result = np.zeros((rows, rows), dtype=int)

    # for i in tqdm(range(rows), desc='Similarity_b_1'):
    #     for j in range(rows):
    #         result[i, j] = round(np.sum(byte_array[i] == byte_array[j])/max_len, 6)
    #         result[j, i] = result[i, j]
    #
    # for i in tqdm(range(rows), desc='Similarity_b_2'):
    #     similarity_b = result[i, :]
    #     similarity_b_list.append(round(sum(similarity_b), 6))

    for i in tqdm(range(seed_num), desc='Similarity_b'):
        similarity_b = []
        for q in range(i):                          # Fill in the lower triangular elements to reduce the time spent traversing each one
            similarity_b.append(similarity_b_matrix[q][i])
        similarity_b.append(1)
        # for j in tqdm(range(seed_num-i-1), desc=f'Similarity_b({i+1}/{seed_num})--->seed {seed_list[i][:9]}'):
        for j in range(seed_num-i-1):
            j += (i + 1)
            similarity_num = 0                      # Number of bytes with the same position and size
            # for t in range(max_len):
            #     if byte_list[i][t] == byte_array[j][t]:
            #         similarity_num += 1
            similarity_num = np.sum(byte_array[i] == byte_array[j])             # Number of bytes with the same position and size
            similarity_b.append(round(similarity_num/max_len, 6))       # The proportion of identical bytes at the same position in seeds i and j
        similarity_b_matrix.append(similarity_b)                        # Update Matrix
        similarity_b_list.append(round(sum(similarity_b), 6))           # Fill in the similarity measure b for the i-th seed
    return similarity_b_list


def similarity(byte_array=None, seed_list=None, max_len=None):
    """
    Compute similarity

    :parameter byte_array: byte sequences
    :parameter seed_list: list of seed name
    :parameter max_len: max length of byte sequences

    :return similarity_list: similarity score(weighted summation)
    """
    a_list = sim_a(byte_array=byte_array, seed_list=seed_list, max_len=max_len)
    b_list = sim_b(byte_array=byte_array, seed_list=seed_list, max_len=max_len)

    h = 0.5    # hyperparameter for weighted summation (h)

    similarity_list = [round(a_list[i] * h + b_list[i] * (1 - h), 6) for i in range(len(seed_list))]
    return similarity_list


def get_index(ele=None, list_src=None):
    """

    :param ele: specify elements
    :param list_src: source list

    :return index_list: The index of ele in the list
    """
    index_list = []
    for i in range(len(list_src)):
        if list_src[i] == ele:
            index_list.append(i)
    return index_list


def order_seed(similarity_list=None, seed_list=None):
    """
    Sort the seeds from low to high based on their similarity

    :param similarity_list: Adaptive similarity list
    :param seed_list: seed name list

    :return seed_list_new: order result
    """
    seed_list_new = []
    similarity_sort = sorted(similarity_list)
    i = 0
    temp = 0                            # Record the current similarity score
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
    Main function in this python file

    :parameter byte_array: byte sequences
    :parameter seed_list: seed name list
    :parameter max_len: max length of byte sequences

    :return similarity_list: mutated seeds list
    """

    """ Compute similarity score """
    similarity_list = similarity(byte_array=byte_array, seed_list=seed_list, max_len=max_len)

    """ Order """
    seed_list_new = order_seed(similarity_list=similarity_list, seed_list=seed_list)

    """ 
        Selecting high-score seeds,
        this is comparing experimental content,
        that's BaSFuzz↓.
    """
    # seed_list_new = chose_bad_seed(seed_list_new)
    # print(len(seed_list_new))
    # print("============")
    # for i in seed_list_new:
    #     print(i)

    return seed_list_new


def order_by_id(seed_list):
    """
    Order seeds by id

    :param seed_list: seed name list
    :return: order results
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


def chose_bad_seed(seed_list):
    """
    Chose high-score seeds

    :param seed_list: seed list
    :return: results
    """
    seed_list = seed_list[int(len(seed_list) / 2):]
    seed_list_new = order_by_id(seed_list)
    return seed_list_new
