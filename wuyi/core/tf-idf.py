#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/16 20:55
# @Author  : jiaguoqing 
# @Email   : jiaguoqing12138@gmail.com
# @File    : tf-idf.py


class tfidf(object):
    """
    将文档转换为 TF-IDF 特征表示
    """
    def __init__(self, text):
        self.text = text
