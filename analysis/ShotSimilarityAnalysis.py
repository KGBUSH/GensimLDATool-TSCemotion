#coding: utf-8

from EmoUtil.EmotionShot import *
from Entity.GlobalValue import *

import time
import os
import exceptions


"""
Created by DY on 2016/06/06
"""


def similarityJaccard(emotionCounter0, emotionCounter1):
    """
    用Jaccard
    相似度计算两个emotionCounter之间的相似度
    :param emotionCounter0:
    :param emotionCounter1:
    :return:
    """
    if len(emotionCounter0) != len(emotionCounter1):
        print('error input in similarityJaccard,emotionCounter0 and emotionCounter1 is not in the same space')
        return
    minSum = 0
    maxSum = 0
    for emotion in emotionCounter0:
        minSum += min(emotionCounter0[emotion], emotionCounter1[emotion])
        maxSum += max(emotionCounter0[emotion], emotionCounter1[emotion])

    simiJ = minSum/maxSum
    return simiJ


def similarityCosine(emotionCounter0, emotionCounter1):
    """
    用Cosine
    计算两个emotionCounter之间的相似度
    :param emotionCounter0:
    :param emotionCounter1:
    :return:
    """
    # if (len(x) != len(y)):
    #     print('error input,x and y is not in the same space')
    #     return;
    # result1 = 0.0;
    # result2 = 0.0;
    # result3 = 0.0;
    # for i in range(len(x)):
    #     result1 += x[i] * y[i]  # sum(X*Y)
    #     result2 += x[i] ** 2  # sum(X*X)
    #     result3 += y[i] ** 2  # sum(Y*Y)
    # # print(result1)
    # # print(result2)
    # # print(result3)
    # print("result is " + str(result1 / ((result2 * result3) ** 0.5)))  # 结果显示(是对的！！)

    if len(emotionCounter0) != len(emotionCounter1):
        print('error input in similarityCosine,emotionCounter0 and emotionCounter1 is not in the same space')
        return
    result1 = 0.0
    result2 = 0.0
    result3 = 0.0
    for emotion in emotionCounter0:
        result1 += emotionCounter0[emotion] * emotionCounter1[emotion]  # sum(X*Y)
        result2 += emotionCounter0[emotion] ** 2  # sum(X*X)
        result3 += emotionCounter1[emotion] ** 2  # sum(Y*Y)

    try:
        simiC = result1/((result2 * result3) ** 0.5)
    except ZeroDivisionError:
        return 0
    return simiC








class ShotSimilarityAnalysis(object):
    """
    shot 情感相似度分析
    考虑movie和shot两个level
    """

    @staticmethod
    def do_SingleShot(shotLocation):
        """
        给出一个具体的shot
        计算其相似度列表
        :param shotLocation: 要计算的shot
        :return:
        """
        print "\n\n*****************************ShotSimilarityAnalysis.do_SingleShot*****************************"
        print "************", shotLocation

        thisShot = EmotionShot(shotLocation=shotLocation)  # 已经把moviesVectors加载到EmotionShot.moviesVectors
        thisShot.emoCalculate4OneShot()  # 这里不用算movieVector,比较的时候直接计算来两个shot的movieVector的Jaccard
        # movieVector已经加载到静态属性里了
        similarityResultsList = []  # 保存相似度计算结果list<tuple(numShot, shotLocation, similarityFactor)>, 这里的shotLocation不是输入参数


        # 直接从'LUTofCorpus.txt'中读取语料库中符合基本条件的shotLocation
        f_LUT = open(os.path.join(GLOBAL_generatedFiles, GLOBAL_LUTofCorpusName), 'r')
        line = f_LUT.readline()

        # 遍历LUTofCorpus.txt
        while line:
            nowNumShot, nowShotLocation = line.split()
            # if int(nowNumShot) % 100 == 0:
            #     print nowNumShot

            nowShot = EmotionShot(shotLocation=nowShotLocation)
            nowShot.emoCalculate4OneShot()

            # 分别计算thisShot和nowShot的 movie-level, shot-level相似度
            movieSimilarity = similarityJaccard(emotionCounter0=EmotionShot.MoviesVectors[thisShot.belongedMovie],
                                                emotionCounter1=EmotionShot.MoviesVectors[nowShot.belongedMovie])
            shotSimilarity = similarityCosine(emotionCounter0=thisShot.shotVector,
                                              emotionCounter1=nowShot.shotVector)

            similarity4TwoShots = movieSimilarity * shotSimilarity
            # 加入similarityResultsList
            similarityResultsList.append(
                (nowNumShot,
                 nowShotLocation[60:],
                 round(movieSimilarity,3),
                 round(shotSimilarity,3),
                 round(similarity4TwoShots,5)
                 )
                                         )
            if int(nowNumShot) % 100 == 0:  # 观察所需
                print nowNumShot, nowShotLocation[60:], round(movieSimilarity,3), round(shotSimilarity,3), round(similarity4TwoShots,5)
            if nowShotLocation == thisShot.shotLocation:
                print nowNumShot, nowShotLocation[60:], round(movieSimilarity,3), round(shotSimilarity,3), round(similarity4TwoShots,5)

            line = f_LUT.readline()


        # 排序：sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
        # key=lambda tupleResult: -tupleResult[*] *是元组的第几个数要确认
        similarityResultsList = sorted(similarityResultsList, key=lambda tupleResult: -tupleResult[4])

        # 输出前**个
        print "打印该shot的相似度结果"
        print2Flie(thisShot=thisShot, similarityResultsList=similarityResultsList)







def print2Flie(thisShot, similarityResultsList):
    """
    把该shot的结果输出到文件
    :param thisShot:
    :param similarityResultsList:
    :return:
    """
    if thisShot.shotLocation.find('/') != -1:  # windows or linux
        saveName = thisShot.belongedMovie + "_" + \
               thisShot.shotLocation[thisShot.shotLocation.rfind('/')+1:]
    else:
        saveName = thisShot.belongedMovie + "_" + \
               thisShot.shotLocation[thisShot.shotLocation.rfind('\\')+1:]

    fw = open(os.path.join(GLOBAL_generatedFiles, saveName), 'w')
    for tupleResult in similarityResultsList[:1000]:
        print tupleResult
        fw.write(tupleResult[0]+"  "+
                 tupleResult[1]+"  "+
                 str(tupleResult[2])+"  "+
                 str(tupleResult[3])+"  "+
                 str(tupleResult[4])+"  "
                 )
        fw.write('\n')
    fw.close()


def getFromFile(fileName):
    """
    批量操作
    :param fileName: 记录specifShots
    :return:
    """
    shotsList = []
    fr = open(fileName, 'r')
    line = fr.readline()
    while line and line != '\n':
        movieName, specifyShotLocation = line.split()
        shotsList.append((movieName, specifyShotLocation))
        line = fr.readline()
    return shotsList








if __name__ == '__main__':
    # shotLocation = GLOBAL_EmotionMovies + '/tragic/1635770suyuan/window/Window301.txt'
    # ShotSimilarityAnalysis.do_SingleShot(shotLocation=shotLocation)

    # 可以考虑每一部电影最多推荐x个shot


    specifyShotFileName = 'C:\\Users\\KGBUS\\PycharmProjects\\GensimLDATool-TSCemotion\\' \
                          'data\\someShots.txt'

    specifyShotsLists = getFromFile(fileName = specifyShotFileName)
    for specifyShot in specifyShotsLists:
        print '\n\n当前时间', time.strftime('%Y-%m-%d %H:%M:%S'), '\n\n'
        ShotSimilarityAnalysis.do_SingleShot(shotLocation=specifyShot[1])



