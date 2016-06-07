# coding: utf-8


import os

# GLOBAL_projectpath = 'C:\\Users\\KGBUS\\PycharmProjects\\GensimLDATool-TSCemotion'
GLOBAL_projectpath = '/home/test/dypaper/GensimLDATool-TSCemotion'
# GLOBAL_projectpath = "E:\\DYwork\\GensimLDATools2.0"

GLOBAL_generatedFiles = GLOBAL_projectpath + '/DY-generatedFiles'

GLOBAL_simiresultsFolder = GLOBAL_generatedFiles + '/similarityResults'
GLOBAL_CECdictFolder = GLOBAL_projectpath + '/data/CECps_Dictionary'
GLOBAL_EmotionMovies = GLOBAL_projectpath + '/data/NewEmotionMovies-2.0'
GLOBAL_DanmukDict = GLOBAL_projectpath + '/data/DanmukDict'


# 初始化语料库
GLOBAL_windowWordsLimit = 3

# 训练LDA的两个参数  # 放在LDAUtil.py
# GLOBAL_numofTopics = 20
# GLOBAL_numofIterations = 200
# 主题输出词个数
GLOBAL_topn = 300

# 输出相似片段的个数
GLOBAL_simioutputnum = 30


GLOBAL_dictionaryName = 'danmaku.dict'
GLOBAL_corporaName = 'danmakuCorpora.mm'
GLOBAL_LUTofCorpusName = 'LUTofCorpus.txt'
GLOBAL_corporaTfidfName = 'danmakuCorporaTfidf.mm'