# coding: utf-8

from collections import *
from Util.InitialCorporaUtil import fill_windowCounter
from Util.StatisticUtil import *





def terrorIndex(emoVector):
    """
    计算movieType == terror 的相关指数，提供一种计算方式
    :param emoVector: <Entity.EmotionWindow.emoVector>
    :return: 指数大小（int）
    """
    beta = [0.4, 0.3, 0.2, 0.1]
    terror = emoVector['anxiety'] * beta[0] + \
             emoVector['sorrow'] * beta[1] +\
             emoVector['hate'] * beta[2] + \
             emoVector['anger'] * beta[3]
    return terror

def funnyIndex(emoVector):
    """
    计算movieType == funny 的相关指数，提供一种计算方式
    :param emoVector: <Entity.EmotionWindow.emoVector>
    :return: 指数大小（int）
    """
    beta = [0.4, 0.3, 0.2, 0.1]
    funny = emoVector['joy'] * beta[0] + \
            emoVector['love'] * beta[1] +\
            emoVector['surprise'] * beta[2] + \
            emoVector['expect'] * beta[3]
    return funny

def intensityIndex(emoVector):
    """
    计算movieType == intensity 的相关指数，提供一种计算方式
    :param emoVector: <Entity.EmotionWindow.emoVector>
    :return: 指数大小（int）
    """
    beta = [0.4, 0.3, 0.2, 0.1]
    intensity = emoVector['surprise'] * beta[0] + \
                emoVector['expect'] * beta[1] +\
                emoVector['love'] * beta[2] + \
                emoVector['joy'] * beta[3]
    return intensity

def tragicIndex(emoVector):
    """
    计算movieType == tragic 的相关指数，提供一种计算方式
    :param emoVector: <Entity.EmotionWindow.emoVector>
    :return: 指数大小（int）
    """
    beta = [0.4, 0.3, 0.2, 0.1]
    tragic = emoVector['sorrow'] * beta[0] + \
             emoVector['hate'] * beta[1] +\
             emoVector['anger'] * beta[2] + \
             emoVector['anxiety'] * beta[3]
    return tragic

def impressiveIndex(emoVector):
    """
    计算movieType == impressive 的相关指数，提供一种计算方式
    :param emoVector: <Entity.EmotionWindow.emoVector>
    :return: 指数大小（int）
    """
    beta = [0.4, 0.3, 0.2, 0.1]
    impressive = emoVector['love'] * beta[0] + \
                 emoVector['joy'] * beta[1] +\
                 emoVector['expect'] * beta[2] + \
                 emoVector['surprise'] * beta[3]
    return impressive







def chooseWindowMovieType(emoVector):
    """
    根据EmotionWindow的emoVector选出这个window的电影类型（五种之一）
    :param emoVector: <Entity.EmotionWindow.emoVector>
    :return: 五种电影情感之一（返回str类型）
    """

    st = StatisticUtil()
    classify = Counter(st.classify)
    classify['terror'] = terrorIndex(emoVector)
    classify['funny'] = funnyIndex(emoVector)
    classify['intensity'] = intensityIndex(emoVector)
    classify['tragic'] = tragicIndex(emoVector)
    classify['impressive'] = impressiveIndex(emoVector)

    movieType = classify.most_common(1)[0][0]
    return movieType



def completeEmotionWindow(windowNum, windowLocation, Emodictionary):
    """
    返回一个完整的Entity.EmotionWindow对象
    :param windowNum: corpus编号
    :param windowLocation: window的位置
    :param Emodictionary: 情感字典
    :return:
    """
    emoWindow = EmotionWindow(windowNum=windowNum, windowLocation=windowLocation)
    # 填充specialwindowList:List<Entity.EmotionWindow>中的emoVector
    for word in emoWindow.wordsCounter:
        for emoword in Emodictionary:
            if word == emoword.word:
                for i in xrange(emoWindow.wordsCounter[word]):
                    emoWindow.update_emoVector(a_word_emotionvector=emoword.emotionVector)
                break
    emoWindow.movieType = chooseWindowMovieType(emoVector=emoWindow.emoVector)
    return emoWindow












class EmotionWindow(object):
    """
    把window加入情感因素
    """

    def __init__(self, windowNum, windowLocation):
        """
        初始化EmotionWindow
        :param windowNum:编号
        :param windowLocation:window位置
        :return:
        """
        self._windowNum = windowNum  #每个window都有一个唯一编号
        self._windowBasicInfo = {'movieName': '', 'movieUrl': '', 'windowLocation': windowLocation}
        self._windowTime = {'startTime': 0, 'endTime': 0}
        self._wordsCounter = Counter()  # 计数这个window中的词
        self._emoVector = Counter()
        self._movieType = ''  # 五种之一
        look_up_table = 'C:\\Users\\KGBUS\\PycharmProjects\\GensimLDATools2.0' \
                        '\\data\\NewEmotionMovies\\movie-xml.data'
        self.deal(windowLocation=windowLocation, lookuptable=look_up_table)



    def deal(self, windowLocation, lookuptable):
        """
        填充EmotionWindow的3个属性
        :param windowLocation: 某special_window的位置
        :param lookuptable: 电影名-url-xml对照表的位置
        :return:
        """
        # windowBasicInfo
        moviename_begin = windowLocation.find('\\', 73) + 1
        moviename_end = windowLocation.find('\\', moviename_begin)
        moviename = windowLocation[moviename_begin: moviename_end]
        fr = open(lookuptable, 'r')
        movieurl = 'no website'
        line = fr.readline()
        while line:
            if moviename in line:
                line = fr.readline()
                movieurl = line.strip('\n')
                break
            line = fr.readline()
        fr.close()
        self._windowBasicInfo['movieName'] = moviename
        self._windowBasicInfo['movieUrl'] = movieurl

        # windowTime
        fr = open(windowLocation, 'r')
        content = fr.read()
        starttime_begin = content.find('startTime') + 11
        starttime_end = content.find('.', starttime_begin)
        starttime = int(content[starttime_begin: starttime_end])
        endtime_begin = content.find('endTime') + 9
        endtime_end = content.find('.', endtime_begin)
        endtime = int(content[endtime_begin: endtime_end])
        self._windowTime['startTime'] = starttime
        self._windowTime['endTime'] = endtime


        # wordsCounter
        fill_windowCounter(windowContent=content, windowCounter=self._wordsCounter)


    @property
    def windowNum(self):
        return self._windowNum

    @property
    def wordsCounter(self):
        return self._wordsCounter

    @property
    def emoVector(self):
        return self._emoVector

    @property
    def movieType(self):
        return self._movieType
    @movieType.setter
    def movieType(self, value):
        self._movieType = value


    def update_emoVector(self, a_word_emotionvector):
        """
        把wordsCounter里面的词的emotionVector，加入到self._emoVector
        :param a_word_emotionvector: Emotionalword的情感向量（Counter）
        :return:
        """
        self._emoVector += a_word_emotionvector


if __name__ == '__main__':
    str1 = 'C:\Users\KGBUS\PycharmProjects\GensimLDATools2.0\data\NewEmotionMovies\impressive\3661452zhiyaonishuoniaiwo2014\window\Window123.txt'