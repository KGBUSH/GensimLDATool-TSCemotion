#coding: utf-8

from Entity.EmotionTopic import *
from Entity.GlobalValue import *
from Util.SimilarityUtil import *
from gensim import corpora, models, similarities



def calculateWordVectorInMaxTopic(maxTopicVector, maxTopicWeight, wordWeightInMaxTopic):
    """
    小论文公式(4) otherwise
    :param maxTopicVector: 权重最大的topic_k的vector
    :param maxTopicWeight: topic_k的权重
    :param wordWeightInMaxTopic: 这个word在topic中的权重
    :return:
    """
    shotWordVector = Counter({'surprise':0, 'sorrow':0, 'love':0, 'joy':0,
                              'hate':0, 'expect':0, 'anxiety':0, 'anger':0,})
    for emotion in shotWordVector:
        shotWordVector[emotion] += round((maxTopicVector[emotion] * maxTopicWeight * (1 + wordWeightInMaxTopic)), 3)
    return shotWordVector





class EmotionShot(object):
    """
    根据论文算法计算shot的emotion
    """

    """
    类属性
    """
    print "********************Loading class attributes**********************"
    print 'Loading TopicInfo'
    topicFile = GLOBAL_generatedFiles + '\\txtall_t10_it500.txt'
    et = EmotionTopic(topicFile)
    _TopicsInfo = et.topicsInfo()
    print 'Loading the Dictionary, LDA and list_corpora, index ...'
    # 载入语料库和lda模型
    myDictLocation = GLOBAL_generatedFiles + '\\' + GLOBAL_dictionaryName
    myCorporaLocation = GLOBAL_generatedFiles + '\\' + GLOBAL_corporaTfidfName
    myLDALocation = GLOBAL_generatedFiles + '\\' + 'topics10___iterations500___.lda'
    _dictionary = corpora.Dictionary.load(myDictLocation)
    _list_corpus = corpora.MmCorpus(myCorporaLocation)
    _lda = models.LdaModel.load(myLDALocation)

    print 'Comunicating the index...'
    # _index是后面检索相似shot用，如果分析单个shot不需要
    _index = similarities.MatrixSimilarity(_lda[_list_corpus])


    def __init__(self, shotLocation):
        """
        参考SimilarityUtil.py
        初始化，dictionanry，LDA
        :return:
        """

        # shot（window）的位置
        self.shotLocation = shotLocation
        self.numofMaxTopic = -1
        self.maxTopicWeight = 0

        # shot Emotion Vector
        self.shotVector = Counter({'surprise':0, 'sorrow':0, 'love':0, 'joy':0,
                              'hate':0, 'expect':0, 'anxiety':0, 'anger':0,})



    def emoCalculate4OneShot(self):
        """
        计算shot_i的情感向量
        :return:
        """
        if self.shotLocation.find('.txt') == -1:
            print 'It is not a windowTXT.'
            return
        fr = open(self.shotLocation, 'r')
        windowContent = fr.read().decode('utf-8', 'ignore').encode('utf-8')  # 忽略繁体字

        windowCounter = Counter()
        Util.InitialCorporaUtil.fill_windowCounter(windowContent, windowCounter)
        listWindowContent = []  # 该shot里的word
        print 'The words in this Shot:'
        for key, count in windowCounter.items():
            for x in xrange(count):
                print key,
                listWindowContent.append(key)
        # 打印shot里words的数量
        print '\nnumbrt of shotwords:',len(listWindowContent)
        vec_bow = EmotionShot._dictionary.doc2bow(listWindowContent)
        vec_lda = EmotionShot._lda[vec_bow]  # 该文档的主题分布

        self.maxTopicWeight = 0
        maxtopic = -1  # 记录shot的权重最大的topic编号
        for tuple_topic in vec_lda:
            if tuple_topic[1] > self.maxTopicWeight:
                self.maxTopicWeight = tuple_topic[1]
                maxtopic = tuple_topic[0]
        self.numofMaxTopic = maxtopic
        print '\nMaxTopic:', self.numofMaxTopic, self.maxTopicWeight



        # 计算该shot的Vector
        print '***************maxTopicInfo*****************'
        EmotionShot.et.show_topic(self.numofMaxTopic)
        self.calculateShotVector(shotWordsList=listWindowContent)




    def calculateShotVector(self, shotWordsList):
        """
        called by emoCalculate4OneShot
        计算Shot 的emotion Vector
        :param shotWordsList: 这个shot的词:list<string>
        :return:
        """
        print '*********************calculating shotVector**********************'

        maxtopicInfo = EmotionShot._TopicsInfo[self.numofMaxTopic]
        count4shotDictWord = 0  # 在dictionary中出现的词
        count4shotTopicWord = 0  # 没在dictionary中找到但是在maxtopic中找到
        count4for = 0
        # 定义两个计数器分别记录词典词的总向量，和topic中的总向量
        shotVector_dict = Counter()
        shotVector_topic = Counter()
        for shotword in shotWordsList:  # 遍历shot中的词
            count4for += 1
            flagfind = False
            for emoword in EmotionShot.et.Emodictionary:
                if emoword.word == shotword:
                    flagfind = True
                    count4shotDictWord += 1
                    # self.shotVector.update(emoword.emotionVector)
                    print 'indict:',emoword.word, emoword.emotionVector
                    shotVector_dict.update(emoword.emotionVector)
                    break
            if not flagfind:  # 没有在词典里找到  # 论文公式4
                for topicItem in maxtopicInfo['topicWords']:
                    if shotword in topicItem:
                        count4shotTopicWord += 1
                        alpha, topicword = topicItem.split('*')
                        alpha = float(alpha)
                        # 论文公式(4) otherwise: 没有在词典找到的词的词向量
                        wordVector = calculateWordVectorInMaxTopic(maxTopicVector=maxtopicInfo['topicVector'],
                                                                   maxTopicWeight=self.maxTopicWeight,
                                                                   wordWeightInMaxTopic=alpha)
                        print '          intopic:',shotword, wordVector
                        # self.shotVector.update(wordVector)
                        shotVector_topic.update(wordVector)
                        break
        print 'count4shotDictWord:', count4shotDictWord
        print 'count4shotTopicWord:', count4shotTopicWord
        print 'shotVector_dict:', shotVector_dict
        print 'shotVector_topic', shotVector_topic

        self.shotVector.update(shotVector_dict)
        self.shotVector.update(shotVector_topic)
        print 'shotVector:', self.shotVector






if __name__ == '__main__':

    print '******************EmotionShot********************'

    # 冒牌家庭
    # shotLocation = 'C:\\Users\\KGBUS\\PycharmProjects\\GensimLDATools2.0\\data\NewEmotionMovies-2.0' \
    #                '\\funny\\2470338maopaijiating\\window\\Window105.txt'
    # 素媛
    # shotLocation = 'C:\\Users\\KGBUS\\PycharmProjects\\GensimLDATools2.0\\data\\NewEmotionMovies-2.0' \
    #                '\\tragic\\1635770suyuan\\window\\Window301.txt'
    # 鬼肆虐
    # shotLocation = 'C:\\Users\\KGBUS\\PycharmProjects\\GensimLDATools2.0\\data\\NewEmotionMovies-2.0' \
    #                '\\terror\\2668234guisinue\\window\\Window145.txt'
    # 魂断蓝桥
    shotLocation = GLOBAL_EmotionMovies + '\\tragic\\1646751hunduanlanqiao\\window\\Window210.txt'


    eShot = EmotionShot(shotLocation=shotLocation)

    eShot.emoCalculate4OneShot()
