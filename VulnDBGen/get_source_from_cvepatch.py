#!/usr/bin/env python
"""
This module retrieves the vulnerable function from cvepatch (diff)
Author: Seulbae Kim (seulbae@korea.ac.kr)
Usage: python get_source_from_cvepatch REPONAME [-m]
    -m: multi-repo mode

[CHANGELOG]
Jul 20    SBKIM    discard comment changes

Aug 08    SBKIM    Major update: with parser (codesensor.jar)
"""

import os
import re
import config
import argparse
import hmark.parseutility as parseutility

# GLOBALS
originalDir = os.getcwd()
diffDir = os.path.join(originalDir, "diff")
chunksCnt = 0  # number of DIFF patches
resultList = []
dummyFunction = parseutility.function(None)
multimodeFlag = 0
gitStoragePath = config.gitStoragePath
gitBinary = config.gitBinary

# ARGUMENTS
parser = argparse.ArgumentParser()
parser.add_argument('REPO',
                    help='''Repository name''')
parser.add_argument('-m', '--multimode', action="store_true",
                    help='''Multimode''')

args = parser.parse_args()

repoName = args.REPO  # name of the directory that holds DIFF patches
if args.multimode:
    multiModeFlag = 1

print "Retrive vulnerable functions from " + repoName + "\nMulti-repo mode: ",
if multimodeFlag:
    print "On"
else:
    print "Off"

# try making missing directories
try:
    os.makedirs(os.path.join(originalDir, 'vul', repoName))
except OSError as e:
    pass

""" re patterns """
pat_src = '[\n](?=diff --git a/)'
pat_chunk = '[\n](?=@@\s[^a-zA-Z]*\s[^a-zA-Z]*\s@@)'
pat_linenum = r"-(\d+,\d+) \+(\d+,\d+) "
pat_linenum = re.compile(pat_linenum)

diffFileCnt = 0
total = len(os.listdir(os.path.join(diffDir, repoName)))
for diffFileName in os.listdir(os.path.join(diffDir, repoName)):    # diffFileName holds the filename of each DIFF patch
    # diffFileName looks like: CVE-2012-2372_7a9bc620049fed37a798f478c5699a11726b3d33.diff
    print str(diffFileCnt+1) + '/' + str(total),
    diffFileCnt += 1

    if os.path.getsize(os.path.join(diffDir, repoName, diffFileName)) > 1000000:
        # don't do anything with big DIFFs (merges, upgrades, ...).
        print "[-]", diffFileName, "\t(file too large)"
    else:
        diffFileNameSplitted = diffFileName.split('_')
        cveId = diffFileNameSplitted[0]    # use only one CVEid
        commitHashValue = diffFileNameSplitted[-1].split('.')[0]

        print "[+]", diffFileName, "\t(proceed)"
        with open(os.path.join(diffDir, repoName, diffFileName), 'r') as fp:
            patchLines = ''.join(fp.readlines())
            patchLinesSplitted = re.split(pat_src, patchLines)
            commitLog = patchLinesSplitted[0]
            affectedFilesList = patchLinesSplitted[1:]

        if multimodeFlag:    # multimode DIFFs have repoPath at the beginning.
            repoPath = commitLog.split('\n')[0]

        numAffectedFiles = len(affectedFilesList)
        for aidx, affectedFile in enumerate(affectedFilesList):
            print "\tFile # " + str(aidx+1) + '/' + str(numAffectedFiles),
            firstLine = affectedFile.split('\n')[0]    # git --diff a/path/filename.ext b/path/filename.ext
            affectedFileName = firstLine.split("--git ")[1].split(" ")[0].split("/")[-1]
            codePath = firstLine.split(' b')[1].strip()    # path/filename.ext

            if not codePath.endswith(".c") and not codePath.endswith(".cpp"):    # and not codePath.endswith('.cc'):
                print "\t[-]", codePath, "(wrong type)"
            else:
                secondLine = affectedFile.split('\n')[1]

                if secondLine.startswith("index") == 0:# or secondLine.endswith("100644") == 0:
                    print "\t[-]", codePath, "(invalid metadata)"    # we are looking for "index" only.
                else:
                    print "\t[+]", codePath
                    indexHashOld = secondLine.split(' ')[1].split('..')[0]
                    indexHashNew = secondLine.split(' ')[1].split('..')[1]

                    chunksList = re.split(pat_chunk, affectedFile)[1:]    # diff file per chunk (in list)
                    chunksCnt += len(chunksList)

                    if multimodeFlag:
                        os.chdir(os.path.join(gitStoragePath, repoName, repoPath))
                    else:
                        os.chdir(os.path.join(gitStoragePath, repoName))
                        # os.chdir(os.path.join("/home/squizz/devgit/", repoName))    #temporary change!!!! Aug 8

                    try:
                        os.remove(originalDir + "/tmp_old")
                        os.remove(originalDir + "/tmp_new")
                    except:
                        pass

                    command_show = "{1} show {2} >> {3}/tmp_old".format(gitBinary, indexHashOld, originalDir)
                    os.system(command_show)
                    command_show = "{1} show {2} >> {3}/tmp_old".format(gitBinary, indexHashNew, originalDir)
                    os.system(command_show)

                    os.chdir(originalDir)
                    oldFunctionInstanceList = parseutility.parseFile_shallow(originalDir + "/tmp_old", "")
                    newFunctionInstanceList = parseutility.parseFile_shallow(originalDir + "/tmp_new", "")

                    finalOldFunctionList = []

                    numChunks = len(chunksList)
                    for ci, chunk in enumerate(chunksList):
                        print "\t\tChunk # " + str(ci+1) + "/" + str(numChunks),

                        chunkSplitted = chunk.split('\n')
                        chunkFirstLine = chunkSplitted[0]
                        chunkLines = chunkSplitted[1:]

                        print chunkFirstLine
                        lineNums = pat_linenum.search(chunkFirstLine)
                        oldLines = lineNums.group(1).split(',')
                        newLines = lineNums.group(2).split(',')
                        
                        offset = int(oldLines[0])
                        pmList = []
                        lnList = []
                        for chunkLine in chunkSplitted[1:]:
                            if len(chunkLine) != 0:
                                pmList.append(chunkLine[0])

                        for i, pm in enumerate(pmList):
                            if pm == ' ' or pm == '-':
                                lnList.append(offset + i)
                            elif pm == '+':
                                lnList.append(offset + i - 1)
                                offset -= 1

                        """ HERE, ADD CHECK FOR NEW FUNCTIONS """
                        hitOldFunctionList = []
                        for f in oldFunctionInstanceList:
                            # print f.lines[0], f.lines[1]

                            for num in range(f.lines[0], f.lines[1]+1):
                                if num in lnList:
                                    # print "Hit at", num
                                    hitOldFunctionList.append(f)
                                    break    # found the function to be patched

                            # if f.lines[0] <= offset <= f.lines[1]:
                            #     print "\t\t\tOffset HIT!!", f.name
                            # elif f.lines[0] <= bound <= f.lines[1]:
                            #     print "\t\t\tBound  HIT!!", f.name

                        for f in hitOldFunctionList:
                            # print "Verify hitFunction", f.name
                            # print "ln",
                            for num in range(f.lines[0], f.lines[1]+1):
                                # print num,
                                try:
                                    listIndex = lnList.index(num)
                                except ValueError:
                                    pass
                                else:
                                    if lnList.count(num) > 1:
                                        listIndex += 1
                                    # print "\nmatch:", num
                                    # print "value\t", chunkSplitted[1:][lnList.index(num)]
                                    # print "pm   \t", pmList[lnList.index(num)]
                                    if pmList[listIndex] == '+' or pmList[listIndex] == '-':
                                        # print "Maybe meaningful",
                                        flag = 0
                                        for commentKeyword in ["/*", "*/", "//", "*"]:
                                            if chunkLines[listIndex][1:].lstrip().startswith(commentKeyword):
                                                flag = 1
                                                break
                                        if flag:
                                            pass
                                            # print "but not."
                                        else:
                                            # print "MEANINGFUL!!"
                                            finalOldFunctionList.append(f)
                                            break
                                    else:
                                        pass
                                        # print "Not meaningful"
                            # print "============\n"

                    finalOldFunctionList = list(set(finalOldFunctionList))    # sometimes list has dups

                    finalNewFunctionList = []
                    for fold in finalOldFunctionList:
                        flag = 0
                        for fnew in newFunctionInstanceList:
                            if fold.name == fnew.name:
                                finalNewFunctionList.append(fnew)
                                flag = 1
                                break
                        if not flag:
                            finalNewFunctionList.append(dummyFunction)

                    # print "\t\t\t", finalOldFunctionList
                    print "\t\t\t", len(finalNewFunctionList), "functions found."
                    vulFileNameBase = diffFileName.split('.diff')[0] + '_' + affectedFileName

                    # os.chdir(os.path.join(originalDir, "vul", repoName))

                    for index, f in enumerate(finalOldFunctionList):
                        os.chdir(originalDir)
                        oldFuncInstance = finalOldFunctionList[index]
                        finalOldFunction = oldFuncInstance.funcBody
                        finalOldFuncId = str(oldFuncInstance.funcId)
                        if finalNewFunctionList[index].name is None:
                            finalNewFunction = ""
                        else:
                            finalNewFunction = finalNewFunctionList[index].funcBody
                        tmpold = parseutility.normalize(parseutility.removeComment(finalOldFunction))
                        tmpnew = parseutility.normalize(parseutility.removeComment(finalNewFunction))

                        if tmpold != tmpnew:
                            # if two are same, it means nothing but comment is patched.
                            os.chdir(os.path.join(originalDir, "vul", repoName))
                            vulOldFileName = vulFileNameBase + '_' + finalOldFuncId + "_OLD.vul"
                            vulNewFileName = vulFileNameBase + '_' + finalOldFuncId + "_NEW.vul"
                            with open(vulOldFileName, 'w') as fp:
                                fp.write(finalOldFunction)
                            with open(vulNewFileName, 'w') as fp:
                                if finalNewFunctionList[index].name is not None:
                                    fp.write(finalNewFunction)
                                else:
                                    fp.write("")
                            os.system("diff -u " + vulOldFileName + " " + vulNewFileName + " >> " + vulFileNameBase + '_' + finalOldFuncId + ".patch")

print ""
print "Done getting vulnerable functions from", repoName
print "Reconstructed", len(
    os.listdir(os.path.join(originalDir, 'vul', repoName))), "vulnerable functions from", diffFileCnt, "patches."
