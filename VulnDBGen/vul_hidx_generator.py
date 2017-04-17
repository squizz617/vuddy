#!/usr/bin/env python

import os
import sys
import hashlib
import time
import argparse
# Import from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import hmark.parseutility as parser


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('REPO',
                    help='''Repository name''')
arg_parser.add_argument('-a', '--abstract-level', type=int,
                    help='''Abstract Level''')
arg_parser.add_argument('-g', '--gran-level',
                    help='''Gran Level''')

args = arg_parser.parse_args()

projName = args.REPO
intendedAbsLvl = 4
intendedGranLvl = 4
if args.abstract_level:
    intendedAbsLvl = args.abstract_level
    if args.gran_level:
        if args.gran_level == 'f':
            intendedGranLvl = 'f'
        else:
            intendedGranLvl = int(args.gran_level)

# if len(sys.argv) == 1:
#    projName = "codeaurora"
#    intendedAbsLvl = 4
#    intendedGranLvl = 4
# else:
#    projName = sys.argv[1]
#    intendedAbsLvl = int(sys.argv[2])
#    intendedGranLvl = sys.argv[3]
# if intendedGranLvl != 'f':
#    intendedGranLvl = int(intendedGranLvl)

projDictList = []
hashFileMapList = []
for i in range(0, 5):
    projDictList.append({})
    hashFileMapList.append({})

print "loading source",
srcFileList = parser.loadVul("./vul/" + projName)
print "(done)"

time0 = time.time()

numFiles = len(srcFileList)
numFuncs = 0
numLines = 0

if intendedGranLvl == 'f':
    for si, srcFile in enumerate(srcFileList):
        print si + 1, '/', len(srcFileList), srcFile
        if intendedAbsLvl == 0:
            functionInstanceList = parser.parseFile_shallow(srcFile, "GUI")
        elif intendedAbsLvl == 4:
            functionInstanceList = parser.parseFile_deep(srcFile, "GUI")
            # Some lines below are added by Squizz on Jan 16, for FP reduction!
            functionInstanceList_New = parser.parseFile_deep(srcFile.replace("OLD.vul", "NEW.vul"), "")

        numFuncs += len(functionInstanceList)
        if len(functionInstanceList) > 0:
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
                projDictList[intendedAbsLvl][funcLen].append(hashValue)
            except KeyError:
                projDictList[intendedAbsLvl][funcLen] = [hashValue]

            try:
                hashFileMapList[intendedAbsLvl][hashValue].extend([f.parentFile, f.funcId])
            except KeyError:
                hashFileMapList[intendedAbsLvl][hashValue] = [f.parentFile, f.funcId]
else:
    for si, srcFile in enumerate(srcFileList):
        print si + 1, '/', len(srcFileList), srcFile
        # TODO: Use parseFile_shallow or parseFile_deep?
        # functionInstanceList = parser.parseFile(srcFile)
        functionInstanceList = parser.parseFile_shallow(srcFile, "")

        numFuncs += len(functionInstanceList)

        if len(functionInstanceList) > 0:
            numLines += functionInstanceList[0].parentNumLoc

        for f in functionInstanceList:
            f.removeListDup()
            path = f.parentFile
            absBody = parser.abstract(f, intendedAbsLvl)[1]
            lineList = []
            for line in absBody.split('\n'):
                normLine = parser.normalize(line)
                if len(normLine) > 1:
                    lineList.append(normLine)

            for lidx in range(0, len(lineList) - intendedGranLvl + 1):
                window = ''.join(lineList[lidx:lidx + intendedGranLvl])
                funcLen = len(window)
                hashValue = hashlib.md5(window).hexdigest()

                try:
                    projDictList[intendedAbsLvl][funcLen].append(hashValue)
                except KeyError:
                    projDictList[intendedAbsLvl][funcLen] = [hashValue]

                try:
                    hashFileMapList[intendedAbsLvl][hashValue].extend([f.parentFile, f.funcId])
                except KeyError:
                    hashFileMapList[intendedAbsLvl][hashValue] = [f.parentFile, f.funcId]

for i in range(0, 5):
    if i == intendedAbsLvl:
        packageInfo = str("3.0.2") + ' ' + str(projName) + ' ' + str(numFiles) + ' ' + str(numFuncs) + ' ' + str(
            numLines) + '\n'
        os.makedirs("hidx-vul-302")
        with open("hidx-vul-302/hashmark_" + str(i) + '_' + projName + ".hidx", 'w') as fp:
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

print "hidx-vul-302/hashmark_" + str(i) + '_' + projName + ".hidx"
time1 = time.time()
print "Elapsed time:", time1 - time0
