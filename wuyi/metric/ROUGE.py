#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/30 19:31
# @Author  : jiaguoqing 
# @Email   : jiaguoqing12138@gmail.com
# @File    : ROUGE.py
""" 计算ROUGE分数 """

from wuyi.metric import rouge_score
from wuyi.tokenizers.BasicTokenizer import BasicTokenizer


class ROUGE:
    DEFAULT_METRICS = ["rouge-1", "rouge-2", "rouge-l"]
    METRICS_FN = {
        "rouge-1": lambda hyp, ref, **k: rouge_score.rouge_n(hyp, ref, 1, **k),
        "rouge-2": lambda hyp, ref, **k: rouge_score.rouge_n(hyp, ref, 2, **k),
        "rouge-l": lambda hyp, ref, **k: rouge_score.rouge_l_summary_level(hyp, ref, **k),
    }
    DEFAULT_STATS = ['f', 'p', 'r']

    def __init__(self, metrics=None, stats=None):
        # metrics
        if metrics is not None:
            self.metrics = [m.lower() for m in metrics]
            for m in self.metrics:
                if m not in ROUGE.DEFAULT_METRICS:
                    raise ValueError("Unknown metric '%s'" % m)
        else:
            self.metrics = ROUGE.DEFAULT_METRICS

        # states
        if stats is not None:
            self.stats = [s.lower() for s in stats]
            for s in self.stats:
                if s not in ROUGE.DEFAULT_STATS:
                    raise ValueError("Unknown stat '%s'" % s)
        else:
            self.stats = ROUGE.DEFAULT_STATS

        # tokenizer
        self.tokenizer = BasicTokenizer()

    def get_scores(self, hyps, refs, avg=False, ignore_empty=False):
        if isinstance(hyps, str):  # 当输入为单条数据，转为List
            hyps, refs = [hyps], [refs]

        if ignore_empty:  # 去掉空值
            hyps_and_refs = [(hyp, ref) for hyp, ref in zip(hyps, refs)
                             if len(hyp) > 0 and len(ref) > 0]
            hyps, refs = zip(*hyps_and_refs)

        assert isinstance(hyps, type(refs)), "type of `hyps` is {}, type of `refs` is {}".format(type(hyps), type(refs))
        assert len(hyps) == len(refs), "length of `hyps` is {}, length of `ref` is {}".format(len(hyps), len(refs))

        if not avg:
            return self._get_scores(hyps, refs)
        return self._get_avg_scores(hyps, refs)

    def _get_scores(self, hyps, refs):
        scores = []
        for hyp, ref in zip(hyps, refs):
            sen_score = {}

            hyp = ' '.join(self.tokenizer.tokenize(hyp))
            ref = ' '.join(self.tokenizer.tokenize(ref))
            hyp = [' '.join(_.split()) for _ in hyp.split('。') if len(_) > 0]
            ref = [' '.join(_.split()) for _ in ref.split('。') if len(_) > 0]

            for m in self.metrics:
                fn = ROUGE.METRICS_FN[m]
                sc = fn(hyp, ref)
                sen_score[m] = {s: sc[s] for s in self.stats}
            scores.append(sen_score)
        return scores

    def _get_avg_scores(self, hyps, refs):
        scores = {m: {s: 0 for s in self.stats} for m in self.metrics}

        count = 0
        for hyp, ref in zip(hyps, refs):
            hyp = ' '.join(self.tokenizer.tokenize(hyp))
            ref = ' '.join(self.tokenizer.tokenize(ref))
            hyp = [' '.join(_.split()) for _ in hyp.split('。') if len(_) > 0]
            ref = [' '.join(_.split()) for _ in ref.split('。') if len(_) > 0]

            for m in self.metrics:
                fn = ROUGE.METRICS_FN[m]
                sc = fn(hyp, ref)
                scores[m] = {s: scores[m][s] + sc[s] for s in self.stats}

            count += 1

        avg_scores = {m: {s: scores[m][s] / count for s in self.stats} for m in self.metrics}
        return avg_scores
