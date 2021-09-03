#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wuyi import ROUGE
from wuyi import BLEU


rouge = ROUGE(metrics='rouge-2', stats='f')
bleu = BLEU()

hyp = "简单测试一下五艺的效果。"
ref = "测试是否能够正确输出。"

rouge_score = rouge.get_scores(hyp, ref, avg=True)
print(rouge_score)

bleu_score = bleu.get_scores(hyp, ref)
print(bleu_score)
