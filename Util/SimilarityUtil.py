# coding: utf-8


from Entity.GlobalValue import *
import Util.InitialCorporaUtil
from Util.StatisticUtil import *

from gensim import corpora, models, similarities

import os
import shutil
import linecache
from collections import *



def saveCorpusSimiResults(numCorpus, lenofCorpora, sort_sims, simi_resultpath):
    """
    把 第numCorpus 篇语料的相似度匹配较高的前30个结果保存到文件
    :param numCorpus: 当前要计算相似度匹配的语料
    :param lenofCorpora: 语料库总数
    :param sort_sims: 得到的相似度结果
    :param simi_resultpath: 要存储的位置
    :return:
    """
    fsim = open(simi_resultpath, 'w')
    if numCorpus % 100 == 0:
        print 'Saving the simiResults of the ' + str(numCorpus) + '/' + str(lenofCorpora) + ' corpus'
    fsim.write('the similarityResults of the ' + str(numCorpus) + ' corpus:' + '\n')
    fsim.write(linecache.getline(GLOBAL_generatedFiles + '\\' + GLOBAL_LUTofCorpusName, numCorpus+1) + '\n\n\n\n\n')
    simnum = 0
    for tup in sort_sims:
        fsim.write(str(tup) + '\n')
        fsim.write(linecache.getline(GLOBAL_generatedFiles + '\\' + GLOBAL_LUTofCorpusName, tup[0]+1) + '\n\n')
        simnum += 1
        if simnum >= GLOBAL_simioutputnum:
            break
    fsim.close()



def saveOnewindowSimiResults(windowLocation, sort_sims, simi_resultpath):
    """
    把 该windowTXT 的相似度匹配较高的前30个结果保存到文件
    :param windowLocation: windowTXT 的位置
    :param sort_sims: 得到的相似度结果
    :param simi_resultpath: 要存储的位置
    :return:
    """
    fsim = open(simi_resultpath, 'w')
    fsim.write('the similarityResults of the ' + windowLocation + ' corpus:' + '\n')
    fsim.write(windowLocation + '\n\n\n\n\n')
    simnum = 0
    for tup in sort_sims:
        fsim.write(str(tup) + '\n')
        fsim.write(linecache.getline(GLOBAL_generatedFiles + '\\' + GLOBAL_LUTofCorpusName, tup[0]+1) + '\n\n')
        simnum += 1
        if simnum >= 30:
            break
    fsim.close()









class SimilarityUtil(object):
    """
    对语料库中每一篇corpus做一次相似度查询，并把结果存入文件
    """
    def __init__(self, myDictLocation, myCorporaLocation, myLDALocation):
        """
        载入相似度查询所需要的 语料库， LDA模型， 并得出index
        :param myCorporaLocation: 语料库的位置
        :param myLDALocation: lda模型的位置
        :return:
        """
        print 'Loading the Dictionary, LDA and list_corpora...'
        self._dictionary = corpora.Dictionary.load(myDictLocation)
        self._list_corpus = corpora.MmCorpus(myCorporaLocation)
        self._lda = models.LdaModel.load(myLDALocation)

        print 'Comunicating the index...'
        self._index = similarities.MatrixSimilarity(self._lda[self._list_corpus])



    @property
    def list_corpora(self):
        return self._list_corpus



    def simiCalculate4Corpora(self, numofCorpus):
        """
        对第numofCorpus篇语料单独做一次相似度计算
        :param numofCorpus:  当前语料在list_corpora中的编号
        :return:
        """

        vec_bow = self._list_corpus[numofCorpus]
        vec_lda = self._lda[vec_bow]  # 该文档的主题分布
        sims = self._index[vec_lda]
        sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])

        simi_resultpath = GLOBAL_simiresultsFolder + '\\sims_corpus' + str(numofCorpus) + '.txt'
        # 存入文件
        saveCorpusSimiResults(numofCorpus, len(self._list_corpus), sort_sims, simi_resultpath)



    def simiCalculate4oneWindow(self, windowLocation, outputName):
        """
        对现有一个windowTxt做一个相似度查询
        :param windowLocation: windowTxt 所在位置
        :param outputName:输出该windowTXT的simiresult的文件名（在generated目录下）
        :return:
        """
        if windowLocation.find('.txt') == -1:
            print 'It is not a windowTXT.'
            return
        fr = open(windowLocation, 'r')
        windowContent = fr.read().decode('utf-8', 'ignore').encode('utf-8')  # 忽略繁体字

        windowCounter = Counter()
        Util.InitialCorporaUtil.fill_windowCounter(windowContent, windowCounter)
        listWindowContent = []
        for key, count in windowCounter.items():
            for x in xrange(count):
                listWindowContent.append(key)

        vec_bow = self._dictionary.doc2bow(listWindowContent)
        vec_lda = self._lda[vec_bow]
        sims = self._index[vec_lda]
        sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])

        simi_resultpath = GLOBAL_generatedFiles + '\\' + outputName
        saveOnewindowSimiResults(windowLocation, sort_sims, simi_resultpath)


    # def corporaClassStatistic(self):
    #     f_LUT = open(GLOBAL_LUTofCorpusName, 'r')
    #     line = f_LUT.readline()
    #     while line:






if __name__ == "__main__":

    # 载入语料库和lda模型
    DictLocation = GLOBAL_generatedFiles + '\\' + GLOBAL_dictionaryName
    CorporaLocation = GLOBAL_generatedFiles + '\\' + GLOBAL_corporaTfidfName
    LDALocation = GLOBAL_generatedFiles + '\\' + 'topics10___iterations500___.lda'
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

