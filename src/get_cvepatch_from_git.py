"""
Created by Squizz on April 10, 2016
This script is for getting cve patches from git object.

CHANGES
AUG 5	SB KIM	(*IMPORTANT*) To maintain the full cve-ids,
                while keeping the filename structure as is,
                I chose to store the mapping in a separate file.
AUG 5	SB KIM	Also, filter the "merge" and "revert" commits first
                in this process.
AUG 15	SB KIM	For multi-repo mode, added the path to the .git object
                at the beginning of each .diff file.
"""

import os
import subprocess
import re
import sys
import time
import pickle

""" GLOBALS """
repoName = None
originalDir = os.getcwd()
diffDir = os.path.join(originalDir, 'diff/')
gitStoragePath = "/media/squizz/VM-mount/data/gitrepos/"
cveDict = pickle.load(open("cvedata.pkl", "rb"))
multiModeFlag = 0
multiRepoList = []

""" FUNCTIONS """


def init():
    # parse arguments, make directories
    global repoName
    global multiModeFlag
    global multiRepoList

    if len(sys.argv) < 2:
        repoName = "linux"
        multiModeFlag = 0
    else:
        repoName = sys.argv[1]
        if len(sys.argv) > 2 and sys.argv[2] == "-m":
            multiModeFlag = 1
            with open("repolists/list_" + repoName) as fp:
                for repoLine in fp.readlines():
                    if len(repoLine) > 2:
                        multiRepoList.append(repoLine.rstrip())
        else:
            multiModeFlag = 0
    if not repoName.endswith("/"):
        repoName += '/'

    print "Retrieving CVE patch from", repoName
    print "Multi-repo mode:",
    if multiModeFlag:
        print "ON."
    else:
        print "OFF."

    print "Initializing...",

    try:
        os.makedirs(diffDir + repoName)
    except:
        pass

    print "Done."


def callGitLog(gitDir):
    # print "Calling git log...",
    grepKeyword = r"'CVE-20'"
    command_log = "git log --all --pretty=fuller --grep=" + grepKeyword

    gitLogOutput = ""
    os.chdir(gitDir)
    try:
        try:
            gitLogOutput = subprocess.check_output(command_log, shell=True)
        except subprocess.CalledProcessError as e:
            print "[-] Git log error:", e
    except UnicodeDecodeError as err:
        print "[-] Unicode error:", err

    # print "Done."
    return gitLogOutput


def filterCommitMessage(commitMessage):
    filterKeywordList = ["merge", "revert", "upgrade"]
    matchCnt = 0
    for kwd in filterKeywordList:
        keywordPattern = r"\W" + kwd + r"\W|\W" + kwd + r"s\W"
        compiledKeyworddPattern = re.compile(keywordPattern)
        match = compiledKeyworddPattern.search(commitMessage.lower())

        # bug fixed.. now revert and upgrade commits will be filtered out.
        if match:
            matchCnt += 1

    if matchCnt > 0:
        return 1
    else:
        return 0


def callGitShow(commitHashValue):
    # print "Calling git show...",
    command_show = "git show --pretty=fuller " + commitHashValue

    try:
        gitShowOutput = subprocess.check_output(command_show, shell=True)
    except subprocess.CalledProcessError as e:
        print "error:", e

    # print "Done."
    return gitShowOutput


def updateCveInfo(cveId):
    # print "Updating CVE metadata...",
    global cveDict

    try:
        cvss = cveDict[cveId][0]
    except:
        cvss = "0.0"
    if len(cvss) == 0:
        cvss = "0.0"

    try:
        cwe = cveDict[cveId][1]
    except:
        cwe = "CWE-000"
    if len(cwe) == 0:
        cwe = "CWE-000"
    else:
        cweNum = cwe.split('-')[1].zfill(3)
        cwe = "CWE-" + str(cweNum)

    # print "Done."
    return cveId + '_' + cvss + '_' + cwe + '_'


def process(gitLogOutput, subRepoName):
    commitsList = re.split('[\n](?=commit\s\w{40}\nAuthor:\s)|[\n](?=commit\s\w{40}\nMerge:\s)', gitLogOutput)
    print len(commitsList), "commits in", repoName,
    if subRepoName is None:
        print "\n"
    else:
        print subRepoName
        os.chdir(os.path.join(gitStoragePath, repoName, subRepoName))

    for commitMessage in commitsList:
        if filterCommitMessage(commitMessage):
            continue
        else:
            commitHashValue = commitMessage[7:47]

            cvePattern = re.compile('CVE-20\d{2}-\d{4}')
            cveIdList = list(set(cvePattern.findall(commitMessage)))

            """	
            Note, Aug 5
            If multiple CVE ids are assigned to one commit,
            store the dependency in a file which is named after
            the repo, (e.g., ~/diff/dependency_ubuntu) and use
            one representative CVE that has the smallest ID number
            for filename.
            A sample:
            CVE-2014-6416_2e9466c84e5beee964e1898dd1f37c3509fa8853	CVE-2014-6418_CVE-2014-6417_CVE-2014-6416_
            """

            if len(cveIdList) > 1:  # do this only if muliple CVEs are assigned to a commit
                fp = open(diffDir + "dependency_" + repoName[:-1], "a")
                cveIdFull = ""
                minimum = 9999
                for cveId in cveIdList:
                    idDigits = int(cveId.split('-')[2])
                    cveIdFull += cveId + '_'
                    if minimum > idDigits:
                        minimum = idDigits
                        minCve = cveId
                fp.write(minCve + '_' + commitHashValue + '\t' + cveIdFull + '\n')
                fp.close()
            elif len(cveIdList) == 0:
                continue
            else:
                minCve = cveIdList[0]

            gitShowOutput = callGitShow(commitHashValue)

            finalFileName = updateCveInfo(minCve)

            print "[+] Writing ", finalFileName + commitHashValue + ".diff",
            try:
                with open(diffDir + repoName + finalFileName + commitHashValue + ".diff", "w") as fp:
                    if subRepoName is None:
                        fp.write(gitShowOutput)
                    else:  # multi-repo mode
                        fp.write(subRepoName + '\n' + gitShowOutput)
            except IOError as e:
                print "Error:", e

            print "Done."


""" main """
t1 = time.time()
init()
if multiModeFlag:
    for sidx, subRepoName in enumerate(multiRepoList):
        gitDir = os.path.join(gitStoragePath, repoName, subRepoName)  # where .git exists
        gitLogOutput = callGitLog(gitDir)
        print str(sidx + 1) + '/' + str(len(multiRepoList))
        if gitLogOutput != "":
            process(gitLogOutput, subRepoName)
else:
    gitDir = os.path.join(gitStoragePath, repoName)  # where .git exists
    gitLogOutput = callGitLog(gitDir)
    process(gitLogOutput, None)

print str(len(os.listdir(diffDir + repoName))) + " patches saved in", diffDir + repoName
print "Done. (" + str(time.time() - t1) + " sec)"
