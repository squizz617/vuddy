#!/usr/bin/env python

import os
import sys
import hashlib
import time
import argparse
from multiprocessing import Pool, Value, Lock
# Import from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import hmark.parseutility as parser


originalDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # vuddy root directory
vulsDir = os.path.join(originalDir, "vul")

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('REPO',
                    help='''Repository name''')
arg_parser.add_argument('-a', '--abstract-level', type=int,
                    help='''Abstract Level''')

args = arg_parser.parse_args()

projName = args.REPO
intendedAbsLvl = 4
if args.abstract_level:
    intendedAbsLvl = args.abstract_level

projDictList = []
hashFileMapList = []
for i in range(0, 5):
    projDictList.append({})
    hashFileMapList.append({})

print "loading source",
srcFileList = parser.loadVul(os.path.join(vulsDir, projName))
print "(done)"

time0 = time.time()

numFiles = len(srcFileList)
numFuncs = 0
numLines = 0

srcFileIdx = Value('i', 0)
lock = Lock()

def parallel_process(srcFile):
    global lock
    global srcFileIdx
    global numFuncs
    global numFiles
    global numLines
    global projDictList
    global hashFileMapList

    with lock:
        srcFileIdx.value += 1
        print srcFileIdx.value, '/', len(srcFileList), srcFile

    if intendedAbsLvl == 0:
        functionInstanceList = parser.parseFile_shallow(srcFile, "")
    elif intendedAbsLvl == 4:
        functionInstanceList = parser.parseFile_deep(srcFile, "")
        # Some lines below are added by Squizz on Jan 16, for FP reduction!
        functionInstanceList_New = parser.parseFile_deep(srcFile.replace("OLD.vul", "NEW.vul"), "")

    with lock:
        numFuncs += len(functionInstanceList)
    if len(functionInstanceList) > 0:
        with lock:
            numLines += functionInstanceList[0].parentNumLoc

    for fi, f in enumerate(functionInstanceList):
        f.removeListDup()
        path = f.parentFile
        absBody = parser.abstract(f, intendedAbsLvl)[1]
        absBody = parser.normalize(absBody)
        # print absBody
        funcLen = len(absBody)
        # print funcLen, absBody
        # print len(absBody)
        hashValue = hashlib.md5(absBody).hexdigest()

        if intendedAbsLvl == 4 and len(functionInstanceList_New) > 0:
            fnew = functionInstanceList_New[fi]
            fnew.removeListDup()
            absBodyNew = parser.abstract(fnew, intendedAbsLvl)[1]
            absBodyNew = parser.normalize(absBodyNew)
            hashValueNew = hashlib.md5(absBodyNew).hexdigest()

            if hashValue == hashValueNew:
                # if abstract bodies of old and new func are identical,
                # don't create hash index
                continue

        try:
            with lock:
                projDictList[intendedAbsLvl][funcLen].append(hashValue)
        except KeyError:
            with lock:
                projDictList[intendedAbsLvl][funcLen] = [hashValue]

        try:
            with lock:
                hashFileMapList[intendedAbsLvl][hashValue].extend([f.parentFile, f.funcId])
        except KeyError:
            with lock:
                hashFileMapList[intendedAbsLvl][hashValue] = [f.parentFile, f.funcId]


#pool = Pool()
#pool.map(parallel_process, srcFileList)
#pool.close()
#pool.join()

for srcFile in srcFileList:
    parallel_process(srcFile)

for i in range(0, 5):
    if i == intendedAbsLvl:
        packageInfo = str("3.0.2") + ' ' + str(projName) + ' ' + str(numFiles) + ' ' + str(numFuncs) + ' ' + str(
            numLines) + '\n'
        hidxDir = os.path.join(vulsDir, "hidx-vul-302")
        if os.path.exists(hidxDir) is False:
            os.makedirs(hidxDir)
        hidxFile = os.path.join(hidxDir, "hashmark_{0}_{1}.hidx".format(i, projName))
        with open(hidxFile, 'w') as fp:
            fp.write(packageInfo)
            for key in sorted(projDictList[i]):
                fp.write(str(key) + '\t')
                for h in list(set(projDictList[i][key])):
                    fp.write(h + '\t')
                fp.write('\n')

            fp.write('\n=====\n')

            for key in sorted(hashFileMapList[i]):
                fp.write(str(key) + '\t')
                for f in hashFileMapList[i][key]:
                    fp.write(str(f) + '\t')
                fp.write('\n')

print os.path.join(vulsDir, "hidx-vul-302", "hashmark_{0}_{1}.hidx".format(i, projName))
time1 = time.time()
print "Elapsed time:", time1 - time0
