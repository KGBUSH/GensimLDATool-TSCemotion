# coding: utf-8

from Entity.EmotionWindow import *
from Entity.GlobalValue import *
from Util.StatisticUtil import StatisticUtil
from Util.ExtractUtil import *
















class EmoSortsimilistUtil(object):
    """
    依据情感词典对 special_window 的相似列表进行再排序
    *special_window: 从all_window中选出部分有特色的window，一般为电影中的高潮部分*
    """

    def __init__(self, specialwindowFile_Location):
        """
        对special_window_list初始化
        :param specialwindowFile_Location: 格式与LUTofCorpus一致，里面存有special_windows
        :return:
        """
        dictfolder = 'C:\\Users\\KGBUS\\PycharmProjects\\GensimLDATools2.0\\data\\CECps_Dictionary'
        self._Emodictionary = ExtractUtil.ExtractEmotionalwordsUtil(dictFolder=dictfolder)  # List<Emotionalword>

        self._specialwindowList = []  # movie1:List<Entity.EmotionWindow>
        self.fillinSpecialwindowList(specialwindowFile_Location)




    def reSortsimiWindow(self):
        """
        对similarity中的 simi_corpus n 的内容进行再排序
        :return:
        """
        numspe_win = 0
        for specialWindow in self._specialwindowList:
            print 'this is', numspe_win, 'th specialWindow :', specialWindow.windowNum
            specialwinNum = specialWindow.windowNum
            simiFileName = 'sims_corpus' + specialwinNum + '.txt'
            simiFileFulName = GLOBAL_simiresultsFolder + '\\' + simiFileName

            # 该emoWindow的相似window列表，顺序无关
            simiList = []  # List<EmotionWindow>
            fr = open(simiFileFulName, 'r')
            line = fr.readline()
            line = fr.readline()
            line = fr.readline()
            numsimi = 0
            while line:
                if 'NewEmotionMovies' not in line:
                    line = fr.readline()
                    continue
                # 找到simiWindow的行
                numWindow, windowLocation = line.split()
                emoWindow = completeEmotionWindow(windowNum=numWindow, windowLocation=windowLocation,
                                                  Emodictionary=self._Emodictionary)
                simiList.append(emoWindow)
                line = fr.readline()
                # 打印 sims_corpusn.txt 中的相似列表数目
                print numsimi,
                numsimi += 1
            print '\n'

            if specialWindow.movieType == 'terror':
                simiList.sort(key=lambda emoWindow: terrorIndex(emoWindow.emoVector), reverse=True)
            if specialWindow.movieType == 'funny':
                simiList.sort(key=lambda emoWindow: funnyIndex(emoWindow.emoVector), reverse=True)
            if specialWindow.movieType == 'intensity':
                simiList.sort(key=lambda emoWindow: intensityIndex(emoWindow.emoVector), reverse=True)
            if specialWindow.movieType == 'tragic':
                simiList.sort(key=lambda emoWindow: tragicIndex(emoWindow.emoVector), reverse=True)
            if specialWindow.movieType == 'impressive':
                simiList.sort(key=lambda emoWindow: impressiveIndex(emoWindow.emoVector), reverse=True)

            for simiwindow in simiList:
                print '编号:', simiwindow.windowNum, specialWindow.movieType,\
                    terrorIndex(simiwindow.emoVector), funnyIndex(simiwindow.emoVector),\
                    intensityIndex(simiwindow.emoVector), tragicIndex(simiwindow.emoVector),\
                    impressiveIndex(simiwindow.emoVector)

            numspe_win += 1
            print '\n'










    def fillinSpecialwindowList(self, fileLoaction):
        """
        把windowFile内容读出并写入specialwindowList
        :param fileLoaction: 文件位置,    里面是要计算的specialwindow的编号和路径，类似LUTofCorpus.txt
        :return:
        """
        print 'the number of SpecialWindow: ',
        num = 0
        fr = open(fileLoaction, 'r')
        line = fr.readline()
        while line:
            if line == '' or line == '\n':
                line = fr.readline()
                continue

            windowNum, windowLocation = line.split()
            # emoWindow 是要处理的specialwindow
            emoWindow = completeEmotionWindow(windowNum=windowNum, windowLocation=windowLocation,
                                              Emodictionary=self._Emodictionary)
            self._specialwindowList.append(emoWindow)
            line = fr.readline()

            print num,
            num += 1
        fr.close()
        print '\n'







if __name__ == '__main__':
    special_location = 'C:\\Users\\KGBUS\\PycharmProjects\\GensimLDATools2.0\\' \
               'DY-generatedFiles\\EmoAnalysis\\specialwindowFile.txt'
    e = EmoSortsimilistUtil(specialwindowFile_Location=special_location)
    e.reSortsimiWindow()

