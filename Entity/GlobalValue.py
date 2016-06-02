# coding: utf-8


import os

GLOBAL_projectpath = 'C:\\Users\\KGBUS\\PycharmProjects\\GensimLDATools2.0'
# GLOBAL_projectpath = "E:\\DYwork\\GensimLDATools2.0"

GLOBAL_generatedFiles = GLOBAL_projectpath + '\\DY-generatedFiles'

GLOBAL_simiresultsFolder = GLOBAL_generatedFiles + '\\similarityResults'
GLOBAL_dictFolder = GLOBAL_projectpath + '\\data\\CECps_Dictionary'

# 初始化语料库
GLOBAL_windowWordsLimit = 3

# 训练LDA的两个参数  # 放在LDAUtil.py
# GLOBAL_numofTopics = 20
# GLOBAL_numofIterations = 200
GLOBAL_topn = 3000

# 输出相似片段的个数
GLOBAL_simioutputnum = 30


GLOBAL_dictionaryName = 'danmaku.dict'
GLOBAL_corporaName = 'danmakuCorpora.mm'
GLOBAL_LUTofCorpusName = 'LUTofCorpus.txt'
GLOBAL_corporaTfidfName = 'danmakuCorporaTfidf.mm'