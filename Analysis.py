from MemAnalysis import *
from CpuAnalysis import *
from JvmAnalysis import *
from StageAnalysis import *

import os

def getFileNames(dirpath, word, filenames):
    for i in os.listdir(dirpath):
        if i.find(word) == 0:
            print i
            filenames.append(dirpath + "/" + i)

logdir = "./logs/NBayes"
cfnames = []
jfnames = []

getFileNames(logdir, "VM", cfnames)
getFileNames(logdir, "JStat", jfnames)

cstats = allCpuStats(cfnames)
#cstats.parse()
cstats.draw_all()
cstats.draw_avg()

jstats = allJvmStats(jfnames)
jstats.draw_gc()
jstats.draw_all()
#jstats.draw_first()

filename = "./logs/spark logs/join_l_log"
stageAnalysisInstance = stageAnalysis(filename)
stageAnalysisInstance.analysis()


