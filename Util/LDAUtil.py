# coding: utf-8



from Entity.GlobalValue import *

from gensim import corpora, models, similarities




def tfidfTransform(list_corpora, list_corporaTfidfLocation):
    """
    把编号化的语料库做一次tfidf
    :param list_corpora: 原始语料库（已编号化）
    :param list_corporaTfidfLocation: 语料库tfidf化后 存储位置
    :return: list_corporaTfidf
    """
    tfidf = models.TfidfModel(list_corpora)
    list_corporaTfidf = tfidf[list_corpora]

    corpora.MmCorpus.serialize(list_corporaTfidfLocation, list_corporaTfidf)
    return list_corporaTfidf



def saveTopicsdetails(lda, numTopics, numIterations):
    """
    # 把主题详情 输入到文本中
    :param numIterations: lda的迭代次数
    :param numTopics: lda的主题个数
    :param lda: lda库
    :return:
    """

    saveTopicsName = "txtall_t" + str(numTopics)\
                 + "_it" + str(numIterations) \
                 + ".txt"
    print "\n\nsaving Topics'detail Distribution to " + GLOBAL_generatedFiles + '\\' + saveTopicsName
    f = open(GLOBAL_generatedFiles + '\\' + saveTopicsName, 'w')

    for i in xrange(numTopics):
        f.write("第" + str(i) + "个topic:\n")
        f.write(lda.print_topic(i,topn=GLOBAL_topn).encode('utf-8'))
        f.write("\n\n")

    f.close()



def saveCorporaTopicsDistribution(corpora_lda):
    """
    # 把corpus_lda写入文件中
    :param corpora_lda:  corpus_lda = lda[corpus_dy_tfidf]  # 得出了主题分布
    :return:
    """

    saveName = 'corpora_themeDistribution.txt'
    print "\n\nsaving Corpora'topics Distribution to " + GLOBAL_generatedFiles + "\\" + saveName
    fw = open(GLOBAL_generatedFiles + "\\" + saveName, 'a')
    fw.truncate()
    docnum = 0
    for doc in corpora_lda:
        docid = "第" +str(docnum) + "篇："
        # print docid
        fw.write(docid + '\n')
        docnum += 1
        # print(doc)
        fw.write(str(doc) + '\n\n')
    fw.close()











class LDAUtil(object):
    """
    该类的作用是读取本地的 字典 和 编号化的语料库
    先对语料库做一次tfidf
    然后根据 语料库和字典 构建lda库
    最后用lda库算出语料库中各个文档的主题分布
    """

    def __init__(self, dictionaryLocation, list_corporaLocation):
        """
        从本地文件中载入 dictionary 和 list_corpora
        :param dictionaryLocation: 字典 的位置
        :param list_corporaLocation: 编号化的语料库（未做tfidf） 的位置
        :return:
        """
        print 'Loading the dictionary and list_corpora'
        self._dictionary = corpora.Dictionary.load(dictionaryLocation)
        self._list_corpora = corpora.MmCorpus(list_corporaLocation)

        self._list_corporaTfidf = []




    def ldaprocess(self, numofTopics, numofIterations):
        """
        lda的处理过程
        :param numofTopics:主题个数
        :param numofIterations: 迭代次数
        :return:
        """
        print 'doing the "tfidf" for the list_corpora...'
        self._list_corporaTfidf = tfidfTransform(self._list_corpora,
                                                 GLOBAL_generatedFiles + '\\' + GLOBAL_corporaTfidfName)
        # 训练LDA模型
        print 'Building LDA model..'
        lda = models.LdaModel(self._list_corporaTfidf, id2word=self._dictionary,
                              num_topics=numofTopics, iterations=numofIterations)

        print 'Saving lda model'
        ldaName = 'topics' + str(numofTopics) + "___" \
              + 'iterations' + str(numofIterations) + "___"\
              + ".lda"
        lda.save(GLOBAL_generatedFiles + '\\' + ldaName)     # 把lda库写入文件，后面要load


        print "一个一个输出："
        for i in xrange(numofTopics):
            print lda.print_topic(i,topn=GLOBAL_topn),type(lda.print_topic(i))
            print '\n'
        saveTopicsdetails(lda, numofTopics, numofIterations)  # 把主题详情写入文件

        corpora_lda = lda[self._list_corporaTfidf]

        saveCorporaTopicsDistribution(corpora_lda)








if __name__ == "__main__":

    GLOBAL_numofTopics = 10
    GLOBAL_numofIterations = 500


    # 字典 和 （编号化）语料库 的存储位置
    dictionaryLocation = GLOBAL_generatedFiles + '\\' + GLOBAL_dictionaryName
    list_corporaLocation = GLOBAL_generatedFiles + '\\' + GLOBAL_corporaName

    mylda = LDAUtil(dictionaryLocation, list_corporaLocation)
    mylda.ldaprocess(numofTopics=GLOBAL_numofTopics, numofIterations=GLOBAL_numofIterations)