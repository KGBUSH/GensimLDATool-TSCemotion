# coding: utf-8


from Entity.GlobalValue import *
import Util.InitialCorporaUtil
from Util.StatisticUtil import *
from Util.LDAUtil import *
from Util.SimilarityUtil import *

from gensim import corpora, models, similarities

import os
import shutil
import linecache
from collections import *



if __name__ == '__main__':
    # 字典 和 （编号化）语料库 的存储位置
    dictionaryLocation = GLOBAL_generatedFiles + '\\' + GLOBAL_dictionaryName
    list_corporaLocation = GLOBAL_generatedFiles + '\\' + GLOBAL_corporaName

    mylda = LDAUtil(dictionaryLocation, list_corporaLocation)
    mylda.ldaprocess(numofTopics=GLOBAL_numofTopics, numofIterations=GLOBAL_numofIterations)

    # 载入语料库和lda模型
    DictLocation = GLOBAL_generatedFiles + '\\' + GLOBAL_dictionaryName
    CorporaLocation = GLOBAL_generatedFiles + '\\' + GLOBAL_corporaTfidfName
    LDALocation = GLOBAL_generatedFiles + '\\' + 'topics20___iterations500___.lda'
    mysimi = SimilarityUtil(myDictLocation=DictLocation,
                            myCorporaLocation=CorporaLocation,
                            myLDALocation=LDALocation)

    print 'Calculating the every corpus similarity results...'
    # 先清空similarityResult文件夹， 再创建
    if os.path.isdir(GLOBAL_simiresultsFolder):
        shutil.rmtree(GLOBAL_simiresultsFolder, True)
    os.makedirs(GLOBAL_simiresultsFolder)
    for x in xrange(len(mysimi.list_corpora)):
        mysimi.simiCalculate4Corpora(numofCorpus=x)


    print '\n\nDoing STATISTIC MODEL........'
    dest = GLOBAL_simiresultsFolder
    mysta = StatisticUtil()
    mysta.buildCorpusList(dest=dest)
    mysta.classStatistics()