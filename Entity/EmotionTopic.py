#coding: utf-8

from collections import *
from Util.ExtractUtil import *


def weight4Topic(alpha):
    """
    类似于一个宏定义，方便做参数调整
    :param alpha: topic_alpha 主题情感的权重，论文公式(3)
    :return:
    """
    return 0.1 + alpha * 50

def topicVectorUpdate(topicVector, emoVector, alpha):
    """
    更新countTopicVector中的topicVector
    :param topicVector: 做累加
    :param emoVector: 能在词典里面找到的词的vector
    :param alpha: word在topic_i中所占权重
    :return:
    """
    # topicVector['surprise'] += emoVector['surprise'] * (1+alpha)
    # topicVector['sorrow'] += emoVector['sorrow'] * (1+alpha)
    # topicVector['love'] += emoVector['love'] * (1+alpha)
    # topicVector['joy'] += emoVector['joy'] * (1+alpha)
    #
    # topicVector['hate'] += emoVector['hate'] * (1+alpha)
    # topicVector['expect'] += emoVector['expect'] * (1+alpha)
    # topicVector['anxiety'] += emoVector['anxiety'] * (1+alpha)
    # topicVector['anger'] += emoVector['anger'] * (1+alpha)

    weight = weight4Topic(alpha)
    for emotion in topicVector:
        topicVector[emotion] += emoVector[emotion] *weight


def topicNormalize(topicVector):
    """
    对topic_i的向量进行归一化处理
    :param topicVector:
    :return:
    """
    maxemo = 0
    for emotion in topicVector:
        topicVector[emotion] = round(topicVector[emotion], 3)
        if topicVector[emotion] > maxemo:
            maxemo = topicVector[emotion]
    for emotion in topicVector:
        topicVector[emotion] = round(topicVector[emotion] / maxemo, 3)

    # 对love,joy进行微调
    topicVector['love'] *= 0.6
    topicVector['joy'] *= 0.8



def countTopicVector(topicWords, EmotionDictionary):
    """
    计算topic_i的emotion_vector
    :param EmotionDictionary: 情感词典# list<Emotionalword>
    :param topicWords: 该topic中的词 list
    :return:
    """
    # topicVector = [0,0,0,0,0,0,0,0]
    topicVector = Counter({'surprise':0, 'sorrow':0, 'love':0, 'joy':0, 'hate':0, 'expect':0, 'anxiety':0, 'anger':0,})
    count4Emoword = 0  # 统计该topic_i中的情感词的数量

    count4for = 0
    for item in topicWords:
        # print count4for,
        count4for += 1

        alpha, topicword = item.split('*')
        alpha = float(alpha)
        findflag = False  # topic_i中这个词是否在词典里面找到
        for emoword in EmotionDictionary:
            if emoword.word == topicword:
                findflag = True
                # print '(find)',
                count4Emoword += 1
                topicVectorUpdate(topicVector=topicVector, emoVector=emoword.emotionVector, alpha=alpha)
                break
    # topicVector 归一化处理
    topicNormalize(topicVector)
    print '\n'
    return count4Emoword, topicVector


class EmotionTopic(object):
    """
    根据txtall_t**_it***.txt，
    计算topic的情感向量，并保存topic信息
    """

    def __init__(self, topicfile):
        """
        初始化，self.TopicsInfoList：list<topic>
        topic = {'topicNum':topicNum, 'topicWords':topicWords, 'topicVector':topicVector,
                 'count4Emoword':count4Emoword, 'topicVector':topicVector}
        :param topicfile: topic文件位置
        :return:
        """
        # 载入情感词典
        dictfolder = 'C:\\Users\\KGBUS\\PycharmProjects\\GensimLDATools2.0\\data\\CECps_Dictionary'
        self.Emodictionary = ExtractUtil.ExtractEmotionalwordsUtil(dictFolder=dictfolder)
        self.EmodictionaryWordList = []  #只装词，不装向量
        for emoword in self.Emodictionary:
            self.EmodictionaryWordList.append(emoword.word)
        print 'Finish loading Emotion-Dictionary..'


        self.TopicsInfoList = []

        fr = open(topicfile, 'r')
        line = fr.readline()
        while line:
            if line == '' or line == '\n':
                line = fr.readline()
                continue
            if 'topic' in line:
                print line,  # 加,是因为line自带'\n'
                topicNum = int(line[3:-10])
                line = fr.readline()
                topicWords = line.split(' + ')
                count4Emoword, topicVector = countTopicVector(topicWords, EmotionDictionary=self.Emodictionary)
                topic = {'topicNum':topicNum, 'topicWords':topicWords,
                         'count4Emoword':count4Emoword, 'topicVector':topicVector}
                self.TopicsInfoList.append(topic)
                line = fr.readline()
                continue
        fr.close()
        return


    def show_topics(self):
        """
        打印topic信息
        :return:
        """
        print "************************topicsInfo************************"
        for topic in self.TopicsInfoList:
            print "topic['topicNum']:",topic['topicNum']
            for word in topic['topicWords']:
                print word,
            print "topic['count4Emoword']:",topic['count4Emoword']
            print "topic['topicVector']:",topic['topicVector']
            print '\n'


    def show_topic(self, numofTopic):
        """
        打印topic信息
        :return:
        """
        print "************************topicInfo************************"
        if numofTopic < 0 or numofTopic >= len(self.TopicsInfoList):
            return
        for topic in self.TopicsInfoList:
            if numofTopic == topic['topicNum']:
                print "topic['topicNum']:",topic['topicNum']
                for word in topic['topicWords']:
                    print word,
                print "topic['count4Emoword']:",topic['count4Emoword']
                print "topic['topicVector']:",topic['topicVector']
                print '\n'
                break


    def topicsInfo(self):
        """
        return结果
        :return:
        """
        return self.TopicsInfoList


if __name__ == '__main__':
    topicfile = 'C:\\Users\\KGBUS\\PycharmProjects\\GensimLDATools2.0\\DY-generatedFiles\\txtall_t10_it500.txt'
    et = EmotionTopic(topicfile)
    et.show_topics()
