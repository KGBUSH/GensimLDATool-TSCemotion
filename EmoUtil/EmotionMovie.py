#coding: utf-8




try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from Entity.DanmukDictionary import *
from Entity.GlobalValue import *

import os
from collections import *
import jieba


class EmotionMovie(object):
    """
    利用从“弹幕多维情感词典.xlsx”提取的
    DanmukDictionary:list<tuple(classification, [wordsList])>
    计算整部movie的整体情感

    最后返回 allEmoMovie:{movieName1:<Counter>, movieName2:<Counter>}  movieName只有名字不包括路径
    """
    """
    类属性：EmotionClassification
    """
    danmakuEmotionCla = ['amazed', 'angry', 'anxiety', 'hate', 'nice', 'sorrow']


    def __init__(self):
        """

        """
        # 文科生弹幕词典的总况
        self.damakDictionaryList = DanmukDictionary.load(danmukDictFolder=GLOBAL_DanmukDict)

        xml_folder = GLOBAL_EmotionMovies

        self.allEmoMovie = {}  # 最后要返回的dict

        for root, dirs, files in os.walk(xml_folder):
            for oneFileName in files:
                if oneFileName.find('.xml') == -1:
                    continue

                oneFullFileName = os.path.join(root, oneFileName)  # 得到每一个.xml完整路径

                # update({movieName_i:<Counter>}), 去掉后面的".xml"
                self.allEmoMovie.update({oneFileName[:-4]: self.calculateEachMovie(oneFullFileName)})




    def calculateEachMovie(self, xmlFile):
        """
        统计每一个movie的情感因子数量
        在 __init__ 中被调用
        :param xmlFile: 一个movie弹幕源文件
        :return:返回一个Counter记录各个维度的emotion
        """
        print xmlFile
        movieCounter = Counter()
        for emotion in EmotionMovie.danmakuEmotionCla:  # Counter初始化
            movieCounter.update({emotion: 0})

        tree = ET.ElementTree(file=xmlFile)
        danmaku_list = []
        for element in tree.iterfind(".//d"):
            # print '第',i, '句'
            # i += 1
            attr = element.get("p")
            sentence = element.text
            if sentence is None:
                continue
            sentence = sentence.encode('utf-8', 'ignore')
            seg_list = jieba.cut(sentence, cut_all=False)  # jieba分词
            for word in seg_list:  # 判断分词是否在Danma情感词典里
                word = word.encode('utf-8', 'ignore')
                for classification in self.damakDictionaryList:
                    if word in classification[1]:
                        wordCla = classification[0]
                        movieCounter[wordCla] += 1  # 如果在词典的某个分类中找到
                        break

        return movieCounter




    def print_allEmoMovie(self):
        """
        打印 allEmoMovie
        :return:
        """

        for (key, value) in self.allEmoMovie.items():
            print key
            print value
            print '\n'




    def calculateEmoMovieVector(self):
        """
        根据统计结果计算Movie-Vector
        1)classification下面的词量
        2)Vector各因子归一化
        :return:
        """
        print "\n\n调整之后的movieVector:"
        claCount4Dict = {}  # 统计词典分类个数 dict:{emotion1:***, emotion2:*** ......}
        for tupleCla in self.damakDictionaryList:
            claCount4Dict.update({tupleCla[0]: tupleCla[2]})

        for movieName, movieCounter in self.allEmoMovie.items():  # 遍历每一部电影
            for emotion in movieCounter:
                movieCounter[emotion] = round(float(movieCounter[emotion])/claCount4Dict[emotion], 3)
            print movieName, movieCounter

        # 归一化向量 as follow （暂时不考虑）





if __name__ == '__main__':
    em = EmotionMovie()
    em.print_allEmoMovie()
    em.calculateEmoMovieVector()


