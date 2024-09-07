#!/usr/bin/env python

import os
import sys
import hashlib
import time
import argparse
import multiprocessing as mp
from functools import partial
# Import from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    import hmark.parseutility as parser
except ImportError:
    import tools.parseutility as parser
import config


def parse_function(absLvl, srcFile):
    if absLvl == 0:
        functionInstanceList = parser.parseFile_shallow(srcFile, "")
        return (srcFile, functionInstanceList, None)
    elif absLvl == 4:
        functionInstanceList = parser.parseFile_deep(srcFile, "")
        # Some lines below are added by Squizz on Jan 16, for FP reduction!
        functionInstanceList_New = parser.parseFile_deep(srcFile.replace("OLD.vul", "NEW.vul"), "")
        return (srcFile, functionInstanceList, functionInstanceList_New)


def main():
    originalDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # vuddy root directory
    vulsDir = os.path.join(originalDir, "vul")

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('REPO',
                            help='''Repository name''')
    arg_parser.add_argument('-a', '--abstract-level', required=True, type=int, nargs=1, choices=[0, 4],
                            help='''Abstract Level''')

    args = arg_parser.parse_args()

    projName = args.REPO
    intendedAbsLvl = 4
    if args.abstract_level:
        intendedAbsLvl = args.abstract_level[0]

    projDictList = []
    hashFileMapList = []
    for i in range(0, 5):
        projDictList.append({})
        hashFileMapList.append({})

    print("loading source"),
    srcFileList = parser.loadVul(os.path.join(vulsDir, projName))
    print("(done)")

    time0 = time.time()

    numFiles = len(srcFileList)
    numFuncs = 0
    numLines = 0

    pool = mp.Pool()
    func = partial(parse_function, intendedAbsLvl)
    for srcFileIdx, returnTuple in enumerate(pool.imap(func, srcFileList)):
        srcFile = returnTuple[0]
        functionInstanceList = returnTuple[1]
        functionInstanceList_New = returnTuple[2]

        print(srcFileIdx + 1, '/', len(srcFileList), srcFile)
        numFuncs += len(functionInstanceList)
        if len(functionInstanceList) > 0:
            numLines += functionInstanceList[0].parentNumLoc

        for fi, f in enumerate(functionInstanceList):
            f.removeListDup()
            path = f.parentFile
            path = "." + path[f.parentFile.find("/vul/"):]
            absBody = parser.abstract(f, intendedAbsLvl)[1]
            #absBody = parser.normalize(absBody).encode('utf-8')
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
                projDictList[intendedAbsLvl][funcLen].append(hashValue)
            except KeyError:
                projDictList[intendedAbsLvl][funcLen] = [hashValue]

            try:
                hashFileMapList[intendedAbsLvl][hashValue].extend([path, f.funcId])
            except KeyError:
                hashFileMapList[intendedAbsLvl][hashValue] = [path, f.funcId]

    pool.close()
    pool.join()

    packageInfo = config.version + ' ' + str(projName) + ' ' + str(numFiles) + ' ' + str(numFuncs) + ' ' + str(
        numLines) + '\n'
    hidxDir = os.path.join(originalDir, "hidx")
    if os.path.exists(hidxDir) is False:
        os.makedirs(hidxDir)
    hidxFile = os.path.join(hidxDir, "hashmark_{0}_{1}.hidx".format(intendedAbsLvl, projName))
    with open(hidxFile, 'w') as fp:
        fp.write(packageInfo)
        for key in sorted(projDictList[intendedAbsLvl]):
            fp.write(str(key) + '\t')
            for h in list(set(projDictList[intendedAbsLvl][key])):
                fp.write(h + '\t')
            fp.write('\n')

        fp.write('\n=====\n')

        for key in sorted(hashFileMapList[intendedAbsLvl]):
            fp.write(str(key) + '\t')
            for f in hashFileMapList[intendedAbsLvl][key]:
                fp.write(str(f) + '\t')
            fp.write('\n')

    print("Hash index saved to:", os.path.join(originalDir, "hidx", "hashmark_{0}_{1}.hidx".format(intendedAbsLvl, projName)))
    time1 = time.time()
    print("Elapsed time:", time1 - time0)


if __name__ == "__main__":
    mp.freeze_support()
    main()
