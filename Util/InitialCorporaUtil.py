# coding:utf-8


from Entity.GlobalValue import *
from Util.ExtractUtil import *
from gensim import corpora, models, similarities

import os
from os.path import join
from collections import *
import shutil
import linecache
from pprint import pprint  # pretty-printer



def fill_windowCounter(windowContent, windowCounter):
    """
    对当前的window.txt 中出现的词做一次汇总 Counter()
    :param windowContent: window.txt文本内容
    :param windowCounter: 计数器
    """
    userFeature_location = windowContent.find('userFeature', 0)
    if userFeature_location == -1:
        return
    windowContent = windowContent[userFeature_location+13: -1]
    if len(windowContent) == 0:
        return

    userDetail_location = windowContent.find('detail', 0)
    while userDetail_location != -1:
        twobrace_location = windowContent.find('}}', userDetail_location)
        userDetail = windowContent[userDetail_location+8: twobrace_location+1]
        windowCounter.update(eval(userDetail))
        userDetail_location = windowContent.find('detail', twobrace_location)



def save_LUTofcorpus(f_LUT, numofCorpus, windowName):
    """
    把texts中的语料编号和对应的文件名存入文件
    :param f_LUT: 文件流
    :param numofCorpus: texts中corpus的序号
    :param windowName: window.txt 的文件名
    :return:
    """
    f_LUT.write(str(numofCorpus) + '\t' + windowName + '\n')









class InitialCorporaUtil(object):
    """
    对 N * windows.txt 中的数据进行读取，生成list_corpora, dictionary.
    并把两个文件存在本地文件。
    """

    def __init__(self):

        print 'Initialization..'
        self._texts = []  # _texts: [[每篇window中的具体的词，用列表存储],[],[]...]
        self._totalWord = 0  # 整个语料库一共多少词汇量，算上重复词语
        self._total_emoword = 0  # 在emotion词典里面出现过得数量，也算上重复

        # 载入情感词典
        dictfolder = GLOBAL_CECdictFolder
        self._Emodictionary = ExtractUtil.ExtractEmotionalwordsUtil(dictFolder=dictfolder)
        self._EmowordsList = []  #只装词，不装向量
        for emoword in self._Emodictionary:
            self._EmowordsList.append(emoword.word)

        self._list_corpora = []  # _list_corpora = [[(),(),()],[],[]....]   最终状态（编号，计数）

        if os.path.isdir(GLOBAL_generatedFiles):
            shutil.rmtree(GLOBAL_generatedFiles, True)
        os.makedirs(GLOBAL_generatedFiles)

        print 'Initialization finished..\n\n'



    def readWindowsTxt(self, dest):
        """
        读取所有window.txt的数据，得到语料库
        :param dest:  windows.txt所在的文件夹
        :return:
        """
        f_LUT = open(GLOBAL_generatedFiles + "/" + GLOBAL_LUTofCorpusName, 'w')  # corpus编号和corpus文件名（含路径）的对照表
        numofCorpus = 0

        print 'Building the _texts...'
        for root, dirs, files in os.walk(dest):
            windowCount4movie = len(files)  # 统计这个电影的window数量
            # 把前三个后三个window排除掉
            headendWindowNum = [0,1,   windowCount4movie-2, windowCount4movie-1]
            numInheadend = 0

            for OneFileName in files:
                if OneFileName.find('.txt') == -1:
                    continue

                if OneFileName in ['Window'+str(i)+'.txt' for i in headendWindowNum]:
                    numInheadend += 1
                    continue
                OneFullFileName = join(root, OneFileName)

                f = open(OneFullFileName)
                # l = f.read().decode('gb2312').encode('utf-8')  #这个在我的测试文件里面是正确的
                # l = f.read().decode('gb2312', 'ignore').encode('utf-8')  # 忽略繁体字
                windowContent = f.read().decode('utf-8', 'ignore').encode('utf-8')  # 忽略繁体字

                windowCounter = Counter()
                fill_windowCounter(windowContent, windowCounter)

                # window.txt没有找到最少限制的words个数 则continue
                if len(windowCounter) <= GLOBAL_windowWordsLimit:
                    continue

                listWindowContent = []
                for key, count in windowCounter.items():
                    for x in xrange(count):
                        listWindowContent.append(key)

                self._texts.append(listWindowContent)
                save_LUTofcorpus(f_LUT, numofCorpus, OneFullFileName)
                numofCorpus += 1
            print root,': -',numInheadend

        f_LUT.close()

        # 剔除稀有数据
        print 'Eliminating the rare data...'
        self._texts = self.delete_rareWords()

        # 情感词汇所占的比重
        # self.count_EmoProportion()



    def savetoDisk(self, dictionaryLocation, corporaLocation):
        """
        根据texts 得到dictionary和_list_corpora
        :param dictionaryLocation: 本地存储字典的文件 位置
        :param corporaLocation: 本地存储语料库（编号化）的文件 位置
        :return:  保存结果到文件
        """

        print 'Building and saving the dictionary...'
        dictionary = corpora.Dictionary(self._texts)
        dictionary.save(dictionaryLocation)

        # 函数doc2bow()简单地对每个不同单词的出现次数进行了计数，并将单词转换为其编号，然后以稀疏向量的形式返回结果
        print 'Building and saving the list_corpora...'
        self._list_corpora = [dictionary.doc2bow(text) for text in self._texts]
        corpora.MmCorpus.serialize(corporaLocation, self._list_corpora)
        # pprint(self._list_corpora)







    def count_EmoProportion(self):
        """
        计算情感词汇占总词汇的比重（观察所需！！！！！！并没有什么用）
        :return:
        """
        print 'Counting the emoword/totalword'
        count_windowlist = 0
        len_texts = len(self._texts)
        noEmowords_Counter = Counter()

        for windowlist in self._texts:
            if count_windowlist % 500 == 0:
                print count_windowlist, '/', len_texts, 'Counting the emoword/totalword'
            count_windowlist += 1

            for word in windowlist:
                self._totalWord += 1
                if word in self._EmowordsList:
                    self._total_emoword += 1
                else:
                    noEmowords_Counter.update({word: 1})

        print '情感词占据的比重:', self._total_emoword, '/', self._totalWord
        print '没有情感对应的词：'
        for item in noEmowords_Counter.most_common(100):
            print item[0], ':', item[1]



    def delete_rareWords(self):
        """
        去除 在整个语料库中仅出现一次的单词
        :return:
        """
        frequency = defaultdict(int)
        for text in self._texts:
            for token in text:
                frequency[token] += 1

        # 这里必须return,否则不能改变实参的值
        return [[token for token in text if frequency[token] > 1] for text in self._texts]








if __name__ == "__main__":
    # dest = 'C:\\Users\\KGBUS\\PycharmProjects\\GensimLDATools\\data\\lzy_severalMovieDanmudata'
    # dest = 'C:\\Users\\KGBUS\\PycharmProjects\\GensimLDATools\\data\EmotionMovie'
    dest = GLOBAL_EmotionMovies

    dictionaryName = GLOBAL_dictionaryName
    corporaName = GLOBAL_corporaName

    mycorpo = InitialCorporaUtil()
    mycorpo.readWindowsTxt(dest)
    mycorpo.savetoDisk(GLOBAL_generatedFiles + '/' + dictionaryName
                       , GLOBAL_generatedFiles + '/' + corporaName)

