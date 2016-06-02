# coding: utf-8


from Entity.GlobalValue import *
import Util.InitialCorporaUtil
from Util.SimilarityUtil import *

from gensim import corpora, models, similarities

import os
import shutil
import linecache
from collections import *



if __name__ == '__main__':
    thefile = 'E:\\DYwork\\GensimLDATools\\_back-up\\generatedFiles\\similarityResults\\sims_corpus11936.txt'

    f = open(thefile, 'r')
    line = f.readline()
    line = f.readline()
    numCorpus, corpusLocation = line.split()
    numCorpus = int(numCorpus)
    print type(numCorpus), corpusLocation
    funny = 0
    impressive = 0
    intensity = 0
    terror = 0
    while line:
        print line
        line = f.readline()
        if 'funny' in line:
            funny += 1
        if 'impressive' in line:
            impressive += 1
        if 'intensity' in line:
            intensity += 1
        if 'terror' in line:
            terror += 1
    f.close()

    print funny, impressive, intensity, terror

    counter = Counter({'funny':43, 'impressive':0, 'intensity':0, 'terror':0})
