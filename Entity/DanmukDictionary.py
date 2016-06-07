# -*- coding: utf-8 -*-


import os



class DanmukDictionary(object):
    """
    从CECps_Dictionary/DanmukDict中读取五大类情感
    词典来源于《文科生》的弹幕多维情感词典.xlsx

    这个词典目前用于做 movieGlobal 的情感向量计算
    """
    @staticmethod
    def load(danmukDictFolder):
        """
        加载
        :param danmukDictFolder:文件夹位置
        :return:
        """
        damakDictionaryList = []  # 元素为 tuple:(classification, list:wordsList, len(wordsList))

        for root, dirs, files in os.walk(danmukDictFolder):
            for oneFileName in files:
                if oneFileName.find('.txt') == -1:
                    continue

                oneFullFileName = os.path.join(root, oneFileName)
                fr = open(oneFullFileName, 'r')
                wordsList = []  # 用以装每个分类下的词
                line = fr.readline()
                while line != '\n':
                    wordsList.append(line.strip())
                    line = fr.readline()

                # wordsList finished
                tuple_class = (oneFileName[:-4], wordsList, len(wordsList))
                damakDictionaryList.append(tuple_class)

        return damakDictionaryList





if __name__ == '__main__':
    folder = '../data/CECps_Dictionary/DanmukDict'
    dList = DanmukDictionary.load(danmukDictFolder=folder)
    print 1