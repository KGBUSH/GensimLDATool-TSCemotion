#coding: utf-8


from analysis.ShotSimilarityAnalysis import *
from EmoUtil.EmotionShot import extractMovieName
from Entity.GlobalValue import *

from collections import *
import time
import os



# 调试用,EmoUtil.EmotionShot import extractMovieName
#
# def extractMovieName(shotLocation):
#     """
#     根据shot地址，抽取所属movieName
#     :param shotLocation: shot地址
#     :return:
#     """
#     # shotLocation = '.../tragic/1646751hunduanlanqiao/window/Window210.txt'
#     windowLocation = shotLocation.find('window')
#     if shotLocation.find('/') != -1:  # windows or linux
#         begin = shotLocation.rfind('/', 0, windowLocation - 2)
#     else:
#         begin = shotLocation.rfind('\\', 0, windowLocation - 2)
#     movieName = shotLocation[begin + 1: windowLocation - 1]
#     return movieName



def getObjShotsFromFile(fileName):
    """
    读入objShots
    :param fileName:
    :return:
    """
    shotsList = []
    fr = open(fileName, 'r')
    line = fr.readline()
    while line :
        if line == '\n' or 'lizhi-movie-xml' not in line:
            line = fr.readline()
            continue
        objShotLocation = line.strip()
        shotsList.append(objShotLocation)
        line = fr.readline()
    return shotsList


def getRecommendFileName(shotLocation, methodName):
    """
    计算 ShotSimilarityAnalysis.do_SingleShot把结果存在哪个文件里面
    :param shotLocation:
    :param methodName:当前测评用的是哪个方法?MTER?CosEV?...
    :return:
    """
    belongedMovie = extractMovieName(shotLocation)
    if shotLocation.find('/') != -1:  # windows or linux
        saveName = belongedMovie + "_" + \
                   shotLocation[shotLocation.rfind('/') + 1:]
    else:
        saveName = belongedMovie + "_" + \
                   shotLocation[shotLocation.rfind('\\') + 1:]
    recommendFileName = 'RankByMovie-' + methodName + '-' + saveName
    return recommendFileName







class Evaluation(object):
    """
    对每个 实验方法 做evaluation
    """

    def __init__(self):
        """
        evaluation indicator
        """
        file4ObjShots = GLOBAL_objectiveShotsFilePath
        self.objShotsList = getObjShotsFromFile(fileName=file4ObjShots)  # list<shotLocation>

        self.indicatorD = {'precision':0, 'recall':0, 'f1':0}
        self.indicatorCounter = Counter()
        # self.MTER_indicatorCounter = Counter(self.indicator)
        # self.CosEV_indicatorCounter = Counter(self.indicator)



    def evaluation(self, method, do_SingleShot_func):
        """
        “类似十字交叉法” 计算方法准确性
        method: MTER
        :param do_SingleShot_func: functionChoice in analysis.ShotSimilarityAnalysis
        :param method: "MTER" or "CosEV" or others , type(str)
        :return:
        """
        self.indicatorCounter.update(self.indicatorD)
        fw = open(os.path.join(GLOBAL_evaluationFolder, 'evaluation-' + method + '.txt'), 'w')
        for oneObjShotLocation in self.objShotsList:
            print '\n\n当前时间', time.strftime('%Y-%m-%d %H:%M:%S'), '\n'
            recommendsList = []

            # 1.ShotSimilarityAnalysis分析，在所有shots中找相似片段集合
            do_SingleShot_func(shotLocation=oneObjShotLocation)

            # 2.找到分析结果所存储的文件.txt,读出结果到 recommendsList = [shotLocation]
            # 下面这句@Test
            #  oneObjShotLocation = '/home/test/dypaper/GensimLDATool-TSCemotion/data' \
            #                      '/lizhi-movie-xml/1949283katejiaolian_p1/window/Window12.txt'
            recommendFileName = getRecommendFileName(shotLocation=oneObjShotLocation, methodName=method)
            fr = open(os.path.join(GLOBAL_evaluationFolder, recommendFileName), 'r')
            line = fr.readline()
            while line:
                if line == '\n' or 'window' not in line:
                    line = fr.readline()
                    continue
                linelist = line.split()
                recommendsList.append(linelist[1])
                line = fr.readline()

            # 3.用self.objShotsList和 recommendsList做查准查全分析
            count = 0
            for shot in self.objShotsList:
                if shot in recommendsList:
                    count += 1
            precision = round(float(count) / len(recommendsList), 4)
            recall = round(float(count) / len(self.objShotsList), 4)
            try:
                f1 = (2 * precision * recall) / (precision + recall)
            except ZeroDivisionError:
                f1 = 0

            indicator4thisObj = {'precision': precision, 'recall': recall, 'f1': f1}
            print indicator4thisObj
            fw.write(str(indicator4thisObj))
            fw.write('\n')

            self.indicatorCounter.update(indicator4thisObj)

        # self.MTER_indicatorCounter 求加权平均
        for factor in self.indicatorCounter:
            self.indicatorCounter[factor] /= len(self.objShotsList)
        print '加权平均后的' + method + '_indicatorCounter:', self.indicatorCounter
        fw.write('加权平均后的' + method + '_indicatorCounter:')
        fw.write(str(self.indicatorCounter))
        fw.write('\n')



















if __name__ == '__main__':
    if not os.path.isdir(GLOBAL_evaluationFolder):
        os.makedirs(GLOBAL_evaluationFolder)
    e = Evaluation()
    # e.evaluation(method='LDA', do_SingleShot_func=ShotSimilarityAnalysis.do_SingleShot_Version2_LDA)
    e.evaluation(method='MTER', do_SingleShot_func=ShotSimilarityAnalysis.do_SingleShot_Version2_MTER)
    # e.evaluation(method='CosEV', do_SingleShot_func=ShotSimilarityAnalysis.do_SingleShot_Version2_CosEV)


