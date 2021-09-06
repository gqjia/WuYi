#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/30 19:30
# @Author  : jiaguoqing 
# @Email   : jiaguoqing12138@gmail.com
# @File    : BLEU.py

import math
import sys
from collections import defaultdict

from wuyi.tokenizers.BasicTokenizer import BasicTokenizer


def _ngram(sent, n_size):
    ngram_list = []
    for left in range(len(sent) - n_size):
        ngram_list.append(sent[left:left + n_size + 1])
    return ngram_list


def get_ngram(sent, n_size, label=None):
    ngram_list = _ngram(sent, n_size)
    if label is not None:
        ngram_list = [ngram + '_' + label for ngram in ngram_list]
    return ngram_list


def get_match_size(hyp_ngram, ref_ngram):
    # ref
    ref_set = defaultdict(int)
    for r_n in ref_ngram:
        tmp_ref_set = defaultdict(int)
        for n in r_n:
            tmp_ref_set[tuple(n)] += 1
        for ngram, count in tmp_ref_set.items():
            ref_set[tuple(ngram)] = max(ref_set[tuple(ngram)], count)
    # for ngram in ref_ngram:
    #     ref_set[tuple(ngram)] += 1

    # hyp
    hyp_set = defaultdict(int)
    for ngram in hyp_ngram:
        hyp_set[tuple(ngram)] += 1

    # match
    match_size = 0
    for ngram, count in hyp_set.items():
        match_size += min(count, ref_set.get(tuple(ngram), 0))  # 匹配次数
    hyp_size = len(hyp_ngram)

    return match_size, hyp_size


class BLEU:
    def __init__(self, n_size=4, weights=None):
        if not weights:
            weights = [1 / n_size for _ in range(n_size)]
        assert len(weights) == n_size, (
                "Number of weights and n-gram should be the same, got Number of weights: '%d' and n-gram: '%d'"
                % (len(weights), n_size))
        self.weights = weights
        self.n_size = n_size
        # tokenizer
        self.tokenizer = BasicTokenizer()

    def get_scores(self, hyps, refs, ignore_empty=False):
        if isinstance(hyps, str):  # 当输入为单条数据，转为List
            hyps, refs = [hyps], [refs]

        if ignore_empty:  # 去掉空值
            hyps_and_refs = [(hyp, ref) for hyp, ref in zip(hyps, refs)
                             if len(hyp) > 0 and len(ref) > 0]
            hyps, refs = zip(*hyps_and_refs)

        assert isinstance(hyps, type(refs)), "type of `hyps` is {}, type of `refs` is {}".format(type(hyps), type(refs))
        assert len(hyps) == len(refs), "length of `hyps` is {}, length of `ref` is {}".format(len(hyps), len(refs))

        return self._get_scores(hyps, refs)

    def _get_scores(self, hyps, refs):
        # add inst
        match_ngram = {}
        candi_ngram = {}
        bp_c = 0
        bp_r = 0
        for hyp, ref in zip(hyps, refs):
            hyp = self.tokenizer.tokenize(hyp)
            if isinstance(ref, list):
                ref = [self.tokenizer.tokenize(r) for r in ref]
            else:
                ref = [self.tokenizer.tokenize(ref)]

            for n_size in range(self.n_size):
                hyp_ngram = get_ngram(hyp, n_size)
                # ref_ngram = get_ngram(ref, n_size)
                refs_ngram = []
                for r in ref:
                    refs_ngram.append(get_ngram(r, n_size))

                if n_size not in match_ngram:
                    match_ngram[n_size] = 0
                    candi_ngram[n_size] = 0
                match_size, hyp_size = get_match_size(hyp_ngram, refs_ngram)
                match_ngram[n_size] += match_size
                candi_ngram[n_size] += hyp_size
            bp_c += len(hyp)
            bp_r += len(ref)

        # Calculate the final bleu metric.
        prob_list = []
        for n_size in range(self.n_size):
            try:
                if candi_ngram[n_size] == 0:
                    _score = 0.0
                else:
                    _score = match_ngram[n_size] / float(candi_ngram[n_size])
            except:
                _score = 0
            if _score == 0:
                _score = sys.float_info.min
            prob_list.append(_score)

        logs = math.fsum(w_i * math.log(p_i) for w_i, p_i in zip(self.weights, prob_list))
        bp = math.exp(min(1 - bp_r / float(bp_c), 0))
        bleu = bp * math.exp(logs)
        return bleu
