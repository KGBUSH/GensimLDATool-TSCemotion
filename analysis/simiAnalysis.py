# coding: utf-8


from Entity.GlobalValue import *
import Util.InitialCorporaUtil
from Util.SimilarityUtil import *

from gensim import corpora, models, similarities

import os
import shutil
import linecache
from collections import *



if __name__ == '__main__':
    # 载入语料库和lda模型
    DictLocation = GLOBAL_generatedFiles + '\\' + GLOBAL_dictionaryName
    CorporaLocation = GLOBAL_generatedFiles + '\\' + GLOBAL_corporaTfidfName
    LDALocation = GLOBAL_generatedFiles + '\\' + 'topics20___iterations500___.lda'
    mysimi = SimilarityUtil(myDictLocation=DictLocation,
                            myCorporaLocation=CorporaLocation,
                            myLDALocation=LDALocation)

    # 计算一个windowTXT的相似度较高的视频片段
    mywinLocation = 'C:\\Users\\KGBUS\PycharmProjects\\dyTSCTools4Python\\' \
                    'data\\movie\\3302411\\window\\Window391.txt'
    outputName = 'xiaoshenke_oldman.txt'
    mysimi.simiCalculate4oneWindow(windowLocation=mywinLocation, outputName=outputName)