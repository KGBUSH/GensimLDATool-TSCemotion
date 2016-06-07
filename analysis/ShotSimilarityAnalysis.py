#coding: utf-8

from EmoUtil.EmotionShot import *
from Entity.GlobalValue import *


import os



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
    # print("result is " + str(result1 / ((result2 * result3) ** 0.5)))  # 结果显示(有错)

    if len(emotionCounter0) != len(emotionCounter1):
        print('error input in similarityCosine,emotionCounter0 and emotionCounter1 is not in the same space')
        return
    result1 = 0.0
    result2 = 0.0
    result3 = 0.0
    for emotion in emotionCounter0:
        result1 += emotionCounter0[emotion] * emotionCounter1[emotion]  # sum(X*Y)
        result2 += emotionCounter0[emotion] ** 2  # sum(X*X)
        result3 += emotionCounter1[emotion  ] ** 2  # sum(Y*Y)

    simiC = result1/(result2**0.5 + result3**0.5)
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
        thisShot = EmotionShot(shotLocation=shotLocation)  # 已经把moviesVectors加载到EmotionShot.moviesVectors
        thisShot.emoCalculate4OneShot()  # 这里不用算movieVector,比较的时候直接计算来两个shot的movieVector的Jaccard
        # movieVector已经加载到静态属性里了
        similarityResultsList = []  # 保存相似度计算结果list<tuple(numShot, shotLocation, similarityFactor)>, 这里的shotLocation不是输入参数


        # 直接从'LUTofCorpus.txt'中读取语料库中符合基本条件的shotLocation
        f_LUT = open(GLOBAL_generatedFiles + "/" + GLOBAL_LUTofCorpusName, 'r')
        line = f_LUT.readline()

        # 遍历LUTofCorpus.txt
        while line:
            nowNumShot, nowShotLocation = line.split()
            if int(nowNumShot) % 100 == 0:
                print nowNumShot

            nowShot = EmotionShot(shotLocation=nowShotLocation)
            nowShot.emoCalculate4OneShot()

            # 分别计算thisShot和nowShot的 movie-level, shot-level相似度
            movieSimilarity = similarityJaccard(emotionCounter0=EmotionShot.MoviesVectors[thisShot.belongedMovie],
                                                emotionCounter1=EmotionShot.MoviesVectors[nowShot.belongedMovie])
            shotSimilarity = similarityCosine(emotionCounter0=thisShot.shotVector,
                                              emotionCounter1=nowShot.shotVector)

            similarity4TwoShots = movieSimilarity * shotSimilarity
            # 加入similarityResultsList
            similarityResultsList.append((nowNumShot, nowShotLocation, similarity4TwoShots))

            line = f_LUT.readline()


        # 排序：sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
        similarityResultsList = sorted(similarityResultsList, key=lambda tupleResult: -tupleResult[2])
        # 输出前30个
        for tupleResult in similarityResultsList[:30]:
            print tupleResult



if __name__ == '__main__':
    shotLocation = GLOBAL_EmotionMovies + '/tragic/1635770suyuan/window/Window301.txt'
    ShotSimilarityAnalysis.do_SingleShot(shotLocation=shotLocation)


