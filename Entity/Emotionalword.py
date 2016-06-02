# coding: utf-8


from collections import *


class Emotionalword(object):
    """
    基于8-dimension情感的词
    """

    def __init__(self, word, emotion_vector):
        """
        为keyword属性赋值
        :return:
        """
        self._word = word  # 词内容
        # word_emotion_vector = [surprise, sorrow, love, joy, hate, expect, anxiety, anger]

        self._emotionVector = Counter()
        self._emotionVector.update({'surprise': emotion_vector['surprise']})
        self._emotionVector.update({'sorrow': emotion_vector['sorrow']})
        self._emotionVector.update({'love': emotion_vector['love']})
        self._emotionVector.update({'joy': emotion_vector['joy']})
        self._emotionVector.update({'hate': emotion_vector['hate']})
        self._emotionVector.update({'expect': emotion_vector['expect']})
        self._emotionVector.update({'anxiety': emotion_vector['anxiety']})
        self._emotionVector.update({'anger': emotion_vector['anger']})


    @property
    def word(self):
        return self._word


    @property
    def emotionVector(self):
        return self._emotionVector

