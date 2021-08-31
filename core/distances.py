#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/16 20:51
# @Author  : jiaguoqing 
# @Email   : jiaguoqing12138@gmail.com
# @File    : distances.py


def elu_distance(vector1, vector2):
    """
    计算两个向量间的欧氏距离。
    """
    x = sum([pow(v1 - v2, 2) for v1, v2 in zip(vector1, vector2)])
    return x
