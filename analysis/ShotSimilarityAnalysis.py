#coding: utf-8

from EmoUtil.EmotionShot import *
from EmoUtil.EmotionShot_CosEV import *
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


#################################################################
def print2File_LDA(thisShotLocation, similarityResultsList):
    """
    把该shot的结果输出到文件，这个函数用的是similarityResultsDict
    :param thisShotLocation:
    :param similarityResultsList:
    :return:
    """
    if thisShotLocation.find('/') != -1:  # windows or linux
        saveName = extractMovieName(thisShotLocation) + "_" + \
                   thisShotLocation[thisShotLocation.rfind('/') + 1:]
    else:
        saveName = extractMovieName(thisShotLocation) + "_" + \
                   thisShotLocation[thisShotLocation.rfind('\\') + 1:]
    saveName = 'RankByMovie-LDA-' + saveName
    recommendCount = GLOBA_LDARecommendShotsCount
    fw = open(os.path.join(GLOBAL_evaluationFolder, saveName), 'w')
    for tupleResult in similarityResultsList[:recommendCount]:
        # print tupleResult
        fw.write(linecache.getline(os.path.join(GLOBAL_generatedFiles, GLOBAL_LUTofCorpusName),
                                   tupleResult[0] + 1))
        fw.write('\n')
    fw.close()





def print2File_MTER_ByMovie(thisShot, similarityResultsDict):
    """
    把该shot的结果输出到文件，这个函数用的是similarityResultsDict
    :param thisShot:
    :param similarityResultsDict:
    :return:
    """
    if thisShot.shotLocation.find('/') != -1:  # windows or linux
        saveName = thisShot.belongedMovie + "_" + \
                   thisShot.shotLocation[thisShot.shotLocation.rfind('/') + 1:]
    else:
        saveName = thisShot.belongedMovie + "_" + \
                   thisShot.shotLocation[thisShot.shotLocation.rfind('\\') + 1:]
    saveName = 'RankByMovie-MTER-' + saveName
    fw = open(os.path.join(GLOBAL_evaluationFolder, saveName), 'w')
    for movie in similarityResultsDict.keys():
        # print movie
        fw.write(movie + '\n')
        recommendCount = min(len(similarityResultsDict[movie]), GLOBAL_count4RecommendFromEachMovie)
        for tupleResult in similarityResultsDict[movie][:recommendCount]:
            # print tupleResult
            fw.write(tupleResult[0] + "  " +
                     tupleResult[1] + "  " +
                     str(tupleResult[2]) + "  " +
                     str(tupleResult[3]) + "  " +
                     str(tupleResult[4]) + "  "
                     )
            fw.write('\n')
        fw.write('\n')
    fw.close()


def print2File_CosEV_ByMovie(thisShot, similarityResultsDict):
    """
    把该shot的结果输出到文件，这个函数用的是similarityResultsDict
    :param thisShot:
    :param similarityResultsDict:
    :return:
    """
    if thisShot.shotLocation.find('/') != -1:  # windows or linux
        saveName = thisShot.belongedMovie + "_" + \
                   thisShot.shotLocation[thisShot.shotLocation.rfind('/') + 1:]
    else:
        saveName = thisShot.belongedMovie + "_" + \
                   thisShot.shotLocation[thisShot.shotLocation.rfind('\\') + 1:]
    saveName = 'RankByMovie-CosEV-' + saveName
    fw = open(os.path.join(GLOBAL_evaluationFolder, saveName), 'w')
    for movie in similarityResultsDict.keys():
        # print movie
        fw.write(movie + '\n')
        recommendCount = min(len(similarityResultsDict[movie]), GLOBAL_count4RecommendFromEachMovie)
        for tupleResult in similarityResultsDict[movie][:recommendCount]:
            # print tupleResult
            fw.write(tupleResult[0] + "  " +
                     tupleResult[1] + "  " +
                     str(tupleResult[2])
                     # str(tupleResult[3]) + "  " +
                     # str(tupleResult[4]) + "  "
                     )
            fw.write('\n')
        fw.write('\n')
    fw.close()



def print2File_all(thisShot, similarityResultsList):
    """
    只适合MTER的输出,     把该shot的结果输出到文件, to be honest, only suit for "ShotSimilarityAnalysis.do_SingleShot"
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
    for tupleResult in similarityResultsList[:100]:
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
                 nowShotLocation,
                 round(movieSimilarity,3),
                 round(shotSimilarity,3),
                 round(similarity4TwoShots,5)
                 )
                                         )
            if int(nowNumShot) % 100 == 0:  # 观察所需
                print nowNumShot, nowShotLocation, round(movieSimilarity,3), round(shotSimilarity,3), round(similarity4TwoShots,5)
            if nowShotLocation == thisShot.shotLocation:
                print nowNumShot, nowShotLocation, round(movieSimilarity,3), round(shotSimilarity,3), round(similarity4TwoShots,5)

            line = f_LUT.readline()


        # 排序：sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
        # key=lambda tupleResult: -tupleResult[*] *是元组的第几个数要确认
        similarityResultsList = sorted(similarityResultsList, key=lambda tupleResult: -tupleResult[4])

        # 输出前**个
        print "打印该shot的相似度结果"
        print2File_all(thisShot=thisShot, similarityResultsList=similarityResultsList)










    @staticmethod
    def do_SingleShot_Version2_MTER(shotLocation):
        """
        给出一个具体的shot
        计算其相似度列表

        这是Version2，相比较前一个版本把 候选shot 全部放入一个similarityResultsDict = {}，
        这里用dict来记录每个电影下面的 候选shot
        :param shotLocation: 要计算的shot
        :return:
        """
        print "\n\n*****************************ShotSimilarityAnalysis.do_SingleShot_Version2_MTER*****************************"
        print "************", shotLocation

        thisShot = EmotionShot(shotLocation=shotLocation)  # 已经把moviesVectors加载到EmotionShot.moviesVectors
        thisShot.emoCalculate4OneShot()  # 这里不用算movieVector,比较的时候直接计算来两个shot的movieVector的Jaccard
        # movieVector已经加载到静态属性里了
        # similarityResultsList = []  # 保存相似度计算结果list<tuple(numShot, shotLocation, similarityFactor)>, 这里的shotLocation不是输入参数

        # 换成Dict方式，目的是为了保存movie名，只记录下每个movie下的排名考前的shot
        similarityResultsDict = {}  # 保存相似度计算结果Dict{movieName: list<tuple(numShot, shotLocation, similarityFactor)>}, 这里的shotLocation不是输入参数

        # 直接从'LUTofCorpus.txt'中读取语料库中符合基本条件的shotLocation
        f_LUT = open(os.path.join(GLOBAL_generatedFiles, GLOBAL_LUTofCorpusName), 'r')
        line = f_LUT.readline()

        # 遍历LUTofCorpus.txt
        while line:
            nowNumShot, nowShotLocation = line.split()
            nowShotMovieName = extractMovieName(shotLocation=nowShotLocation)
            if nowShotMovieName not in similarityResultsDict.keys():  # 如果还没有这个movie，加入字典
                similarityResultsDict[nowShotMovieName] = []
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

            # 加入similarityResultsDist中对应的movie下面
            similarityResultsDict[nowShotMovieName].append(
                (nowNumShot,
                 nowShotLocation,
                 round(movieSimilarity, 3),
                 round(shotSimilarity, 3),
                 round(similarity4TwoShots, 5)
                 )
            )
            if int(nowNumShot) % 100 == 0:  # 观察所需
                print nowNumShot, nowShotLocation, round(movieSimilarity, 3), \
                    round(shotSimilarity, 3), round(similarity4TwoShots, 5)
            if nowShotLocation == thisShot.shotLocation:
                print nowNumShot, nowShotLocation, round(movieSimilarity, 3), \
                    round(shotSimilarity, 3), round(similarity4TwoShots, 5)

            line = f_LUT.readline()

        # 排序：sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
        # key=lambda tupleResult: -tupleResult[*] *是元组的第几个数要确认
        for movie in similarityResultsDict.keys():
            similarityResultsDict[movie] = sorted(similarityResultsDict[movie], key=lambda tupleResult: -tupleResult[4])

        # 输出前**个
        print "打印该shot的相似度结果"
        print2File_MTER_ByMovie(thisShot=thisShot, similarityResultsDict=similarityResultsDict)









    @staticmethod
    def do_SingleShot_Version2_CosEV(shotLocation):
        """
        给出一个具体的shot
        计算其相似度列表

        这是Version2，相比较前一个版本把 候选shot 全部放入一个similarityResultsDict = {}，
        这里用dict来记录每个电影下面的 候选shot
        :param shotLocation: 要计算的shot
        :return:
        """
        print "\n\n*****************************ShotSimilarityAnalysis.do_SingleShot_Version2_CosEV*****************************"
        print "************", shotLocation

        thisShot = EmotionShot_CosEV(shotLocation=shotLocation)  # 已经把moviesVectors加载到EmotionShot.moviesVectors
        thisShot.emoCalculate4OneShot()  # 这里不用算movieVector,比较的时候直接计算来两个shot的movieVector的Jaccard
        # movieVector已经加载到静态属性里了
        # similarityResultsList = []  # 保存相似度计算结果list<tuple(numShot, shotLocation, similarityFactor)>, 这里的shotLocation不是输入参数

        # 换成Dict方式，目的是为了保存movie名，只记录下每个movie下的排名考前的shot
        similarityResultsDict = {}  # 保存相似度计算结果Dict{movieName: list<tuple(numShot, shotLocation, similarityFactor)>}, 这里的shotLocation不是输入参数

        # 直接从'LUTofCorpus.txt'中读取语料库中符合基本条件的shotLocation
        f_LUT = open(os.path.join(GLOBAL_generatedFiles, GLOBAL_LUTofCorpusName), 'r')
        line = f_LUT.readline()

        # 遍历LUTofCorpus.txt
        while line:
            nowNumShot, nowShotLocation = line.split()
            nowShotMovieName = extractMovieName(shotLocation=nowShotLocation)
            if nowShotMovieName not in similarityResultsDict.keys():  # 如果还没有这个movie，加入字典
                similarityResultsDict[nowShotMovieName] = []
            # if int(nowNumShot) % 100 == 0:
            #     print nowNumShot

            nowShot = EmotionShot_CosEV(shotLocation=nowShotLocation)
            nowShot.emoCalculate4OneShot()

            # 只用计算 shot-level相似度
            # movieSimilarity = similarityJaccard(emotionCounter0=EmotionShot.MoviesVectors[thisShot.belongedMovie],
            #                                     emotionCounter1=EmotionShot.MoviesVectors[nowShot.belongedMovie])
            shotSimilarity = similarityCosine(emotionCounter0=thisShot.shotVector,
                                              emotionCounter1=nowShot.shotVector)
            similarity4TwoShots = shotSimilarity

            # 加入similarityResultsDist中对应的movie下面
            similarityResultsDict[nowShotMovieName].append(
                (nowNumShot,
                 nowShotLocation,
                 # round(movieSimilarity, 3),
                 # round(shotSimilarity, 3),
                 round(similarity4TwoShots, 5)
                 )
            )
            if int(nowNumShot) % 100 == 0:  # 观察所需
                print nowNumShot, nowShotLocation, round(similarity4TwoShots, 5)
            if nowShotLocation == thisShot.shotLocation:
                print nowNumShot, nowShotLocation, round(similarity4TwoShots, 5)

            line = f_LUT.readline()

        # 排序：sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
        # key=lambda tupleResult: -tupleResult[*] *是元组的第几个数要确认
        for movie in similarityResultsDict.keys():
            similarityResultsDict[movie] = sorted(similarityResultsDict[movie], key=lambda tupleResult: -tupleResult[2])

        # 输出前**个
        print "打印该shot的相似度结果"
        print2File_CosEV_ByMovie(thisShot=thisShot, similarityResultsDict=similarityResultsDict)








    @staticmethod
    def do_SingleShot_Version2_LDA(shotLocation):
        """
        给出一个具体的shot
        计算其相似度列表, 用LDA
        :param shotLocation: 要计算的shot
        :return:
        """
        print "\n\n*****************************ShotSimilarityAnalysis.do_SingleShot_Version2_LDA*****************************"
        print "************", shotLocation

        # 1.确定shotLocation的编号
        fr = open(os.path.join(GLOBAL_generatedFiles, GLOBAL_LUTofCorpusName), 'r')
        line = fr.readline()
        num4Shot = -1
        while line:  # 在GLOBAL_LUTofCorpusName找到编号
            if shotLocation in line:
                num4Shot = line.split()[0]
                num4Shot = int(num4Shot)  #必须转换成int
                break
            line = fr.readline()
        if num4Shot == -1:
            print "do_SingleShot_Version2_LDA: can not find the num4Shot in LUTofCorpusName", shotLocation
            return

        # 2.gensim API (参考 SimilarityUtil.simiCalculate4Corpora),可以得到排好名的rankList
        vec_bow = EmotionShot._list_corpus[num4Shot]
        vec_lda = EmotionShot._lda[vec_bow]
        sims = EmotionShot._index[vec_lda]
        similarityResultsList = sorted(enumerate(sims), key=lambda item: -item[1])

        # 3.打印前 n 个到文件,(调用print2File)
        # 输出前**个
        print "打印该shot的相似度结果"
        print2File_LDA(thisShotLocation=shotLocation, similarityResultsList=similarityResultsList)










if __name__ == '__main__':
    # shotLocation = GLOBAL_EmotionMovies + '/tragic/1635770suyuan/window/Window301.txt'
    # ShotSimilarityAnalysis.do_SingleShot(shotLocation=shotLocation)

    # 可以考虑每一部电影最多推荐x个shot


    # specifyShotFileName = 'C:\\Users\\KGBUS\\PycharmProjects\\GensimLDATool-TSCemotion\\' \
    #                       'data\\someShots.txt'
    specifyShotFileName = '/home/test/dypaper/GensimLDATool-TSCemotion/data/someShots-linux.txt'

    specifyShotsLists = getFromFile(fileName = specifyShotFileName)
    for specifyShot in specifyShotsLists:
        print '\n\n当前时间', time.strftime('%Y-%m-%d %H:%M:%S'), '\n\n'
        ShotSimilarityAnalysis.do_SingleShot_Version2(shotLocation=specifyShot[1])



