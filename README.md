# 五艺（WuYi）
五艺是一个简易的中文自然语言处理工具  
主要包括的功能有：中文分词、词性标注、情感分析、命名实体识别、关系抽取、关键词抽取、文本摘要、新词发现、文本聚类。  
当前还在开发中。  

## 安装
使用pip安装
```shell
pip install WuYi
```

## 中文分词
```python
from wuyi import BasicTokenizer


tokenizer = BasicTokenizer()
text = "测试中文分词效果。"
tokens = tokenizer.tokenize(text=text)

print(tokens)
```

## 评价指标
```python
from wuyi import ROUGE, BLEU


rouge = ROUGE()
bleu = BLEU()

hyp = "简单测试一下五艺的效果。"
ref = "测试是否能够正确输出。"

rouge_score = rouge.get_scores(hyp, ref, avg=True)
print(rouge_score)

bleu_score = bleu.get_scores(hyp, ref)
print(bleu_score)
```


## 开发进度
中文分词【10%】  
词性标注【0%】  
情感分析【0%】  
命名实体识别【0%】  
关系抽取【0%】  
关键词抽取【0%】  
文本摘要【0%】  
新词发现【0%】  
文本聚类【1%】  
评测指标【20%】


## 文档结构
```text
\examples  示例代码
\wuyi  
    \clustering  聚类算法[未完成]
        kmeans.py  K-Means算法[未完成]
    \core  核心部分代码[未完成]
    \tokenizers 分词部分代码[未完成]
        BasicTokenizer.py 基础分词[完成]
    \metric  指标部分代码[未完成]
        BLEU.py  bleu评测指标[完成]
        ROUGE.py  rouge评测指标[完成]
```
