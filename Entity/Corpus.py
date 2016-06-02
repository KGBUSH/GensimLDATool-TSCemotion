# coding: utf-8


from Entity.GlobalValue import *



class Corpus(object):
    """
    用于描述corpus的分类（funny,impressive,...）,相似列表中的分类百分比
    数据源于 GLOBAL_simiresultsFolder

    *只在StatisticUtil中会用到，作统计分析*
    """

    def __init__(self, numcorpus, corpuslocation, classification):
        """
        初始化 corpus对象
        :param numcorpus: corpus编号
        :param corpuslocation: corpus位置
        :param classification: corpus的归类
        :return:
        """
        self.numCorpus = numcorpus
        self.corpusLocation = corpuslocation
        self.classification = classification

        # 相似度排名中的corpus占四个分类的 百分比
        self.ratioFunny = 0.0
        self.ratioImpressive = 0.0
        self.ratioIntensity = 0.0
        self.ratioTerror = 0.0
        self.ratioTragic = 0.0

    def countRatio(self, numfunny, numimpressive, numintensity, numterror, numtragic):
        """
        对四个ratio赋值，保留三位小数
        :param numfunny:
        :param numimpressive:
        :param numintensity:
        :param numterror:
        :param numtragic:
        :return:
        """
        self.ratioFunny = round(float(numfunny)/GLOBAL_simioutputnum, 3)
        self.ratioImpressive = round(float(numimpressive)/GLOBAL_simioutputnum, 3)
        self.ratioIntensity = round(float(numintensity)/GLOBAL_simioutputnum, 3)
        self.ratioTerror = round(float(numterror)/GLOBAL_simioutputnum, 3)
        self.ratioTragic = round(float(numtragic)/GLOBAL_simioutputnum, 3)