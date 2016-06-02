# coding: utf-8

from Entity.Emotionalword import *
from collections import *

import os
from os.path import join





class ExtractUtil(object):

    @staticmethod
    def ExtractEmotionalwordsUtil(dictFolder):
        """
        从目标文件夹中读取出情感字典并用Entity.Emotionalword接收
        :param dictFolder: 目标文件夹
        :return:
        """
        print 'Now read-in the emotional words from Dictionary..'
        Emodictionary = []  # list<Emotionalword>
        for root, dirs, files in os.walk(dictFolder):
            for OneFileName in files:
                if OneFileName.find('dict') == -1 and OneFileName.find('.txt') == -1:
                    continue
                OneFullFileName = join(root, OneFileName)
                fr = open(OneFullFileName, 'r')
                line = fr.readline()
                while line:
                    if line == '' or line == '\n':
                        line = fr.readline()
                        continue
                    word, num, strdict = line.split('  ,  ')
                    word_emotionVector = Counter(eval(strdict))
                    emoWord = Emotionalword(word=word, emotion_vector=word_emotionVector)
                    Emodictionary.append(emoWord)
                    line = fr.readline()
                fr.close()
        print 'read-in', len(Emodictionary), 'emotional words.'
        return Emodictionary





if __name__ == '__main__':
    dictFolder = 'C:\\Users\\KGBUS\\PycharmProjects\\GensimLDATools2.0\\data\\CECps_Dictionary'
    ExtractUtil.ExtractEmotionalwordsUtil(dictFolder=dictFolder)