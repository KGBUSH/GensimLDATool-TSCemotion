# coding: utf-8


from Entity.GlobalValue import *
from Entity.Corpus import *

import os
from os.path import join
import shutil
from collections import *



class StatisticUtil(object):
    """
    对相似度结果进行统计分析
    """
    def __init__(self):
        """
        初始化 分类详情
        初始化 corpusList：[corpus, corpus,...]
        :return:
        """
        # sentiment classification，可扩展
        self.classify = Counter({'funny':0, 'impressive':0, 'intensity':0, 'terror':0, 'tragic':0})
        self.corpusList = []  # list<corpus>


    def buildCorpusList(self, dest):
        """
        把相似度结果读入到corpusList：[corpus, corpus,...]
        :return:
        """
        print '<StatisticUtil> Building the corpusList...\n'
        for root, dirs, files in os.walk(dest):
            for OneFileName in files:
                if OneFileName.find('.txt') == -1:
                    continue
                OneFullFileName = join(root, OneFileName)

                f_cla = open(OneFullFileName, 'r')
                line = f_cla.readline()
                line = f_cla.readline()
                numCorpus, corpusLocation = line.split()
                numCorpus = int(numCorpus)
                for item in self.classify:
                    if item in corpusLocation:
                        corpus = Corpus(numCorpus, corpusLocation, classification=item)
                        break

                corpusCounter = Counter(self.classify)
                while line:
                    line = f_cla.readline()
                    for emotiontype in corpusCounter:
                        if emotiontype in line:
                            corpusCounter[emotiontype] += 1
                            break

                f_cla.close()
                corpus.countRatio(numfunny=corpusCounter['funny'], numimpressive=corpusCounter['impressive'],
                                  numintensity=corpusCounter['intensity'], numterror=corpusCounter['terror'],
                                  numtragic=corpusCounter['tragic'])

                self.corpusList.append(corpus)




    def classStatistics(self):
        """
        分别统计四种情感，计算占有率
        :return:
        """
        print '<StatisticUtil> counting the ratio Statistics...\n'
        for classification in self.classify:
            countCla = 0
            claCounter = Counter(self.classify)

            for corpus in self.corpusList:  # 每次都重新遍历一遍self.corpusList: list<corpus>
                if corpus.classification == classification:
                    countCla += 1
                    claCounter['funny'] += corpus.ratioFunny
                    claCounter['impressive'] += corpus.ratioImpressive
                    claCounter['intensity'] += corpus.ratioIntensity
                    claCounter['terror'] += corpus.ratioTerror
                    claCounter['tragic'] += corpus.ratioTragic

            raFunny = round(float(claCounter['funny'])/countCla, 3)
            raImpressive = round(float(claCounter['impressive'])/countCla, 3)
            raIntensity = round(float(claCounter['intensity'])/countCla, 3)
            raTerror = round(float(claCounter['terror'])/countCla, 3)
            raTragic = round(float(claCounter['tragic'])/countCla, 3)
            print 'the classification: ', classification
            print 'the number of corpus is: ', countCla
            print 'ratioFunny: ', raFunny
            print 'ratioImpressive: ', raImpressive
            print 'ratioIntensity: ', raIntensity
            print 'ratioTerror: ', raTerror
            print 'ratioTragic: ', raTragic
            print '\n'



if __name__ == '__main__':
    print '\n\nDoing STATISTIC MODEL........'
    dest = GLOBAL_simiresultsFolder
    mysta = StatisticUtil()
    mysta.buildCorpusList(dest=dest)
    mysta.classStatistics()