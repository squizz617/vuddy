"""
Created by Squizz on April 10, 2016
This script is for getting cve patches from git object.
Last modified: August 5, 2016

CHANGES
AUG 5   SB KIM  (*IMPORTANT*) To maintain the full cve-ids,
                while keeping the filename structure as is,
                I chose to store the mapping in a separate file.
AUG 5   SB KIM  Also, filter the "merge" and "revert" commits first
                in this process.
AUG 15  SB KIM  For multi-repo mode, added the path to the .git object
                at the beginning of each .diff file.
"""

import os
import subprocess
import re
import time

try:
    import cPickle as pickle
except:
    import pickle
import argparse
import config

""" GLOBALS """
repoName = None
originalDir = os.getcwd()
diffDir = os.path.join(originalDir, 'diff/')
cveDict = pickle.load(open("cvedata.pkl", "rb"))
multiModeFlag = 0
multiRepoList = []
gitStoragePath = config.gitStoragePath
gitBinary = config.gitBinary


""" FUNCTIONS """
def parse_argument():
    """
    Parse arguments
    :return: nothing
    """
    global repoName
    global multiModeFlag
    global multiRepoList

    parser = argparse.ArgumentParser(prog='get_cvepatch_from_git.py')
    parser.add_argument('REPO',
                        help='''Repository name''')
    parser.add_argument('-m', '--multimode', action="store_true",
                        help='''Multimode''')

    args = parser.parse_args()

    repoName = args.REPO
    if args.multimode:
        multiModeFlag = 1
        with open("repolists/list_" + repoName) as fp:
            for repoLine in fp.readlines():
                if len(repoLine) > 2:
                    multiRepoList.append(repoLine.rstrip())
    else:
        multiModeFlag = 0


def init():
    """
    Make directories
    :return: Nothing
    """
    global repoName
    global multiModeFlag
    global multiRepoList

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
    """
    Collect CVE commit log from repository
    :param gitDir: repository path
    :return:
    """
    # print "Calling git log...",
    global gitBinary

    grepKeyword = r"'CVE-20'"
    command_log = "{0} log --all --pretty=fuller --grep={1}".format(gitBinary, grepKeyword)

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
    """
    Filter false positive commits 
    Will remove 'Merge', 'Revert', 'Upgrade' commit log
    :param commitMessage: commit message
    :return: 
    """
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
    """
    Grep data of git show
    :param commitHashValue: 
    :return: 
    """
    # print "Calling git show...",
    command_show = "{0} show --pretty=fuller {1}".format(gitBinary, commitHashValue)

    try:
        gitShowOutput = subprocess.check_output(command_show, shell=True)
    except subprocess.CalledProcessError as e:
        print "error:", e

    # print "Done."
    return gitShowOutput


def updateCveInfo(cveId):
    """
    Get CVSS score and CWE id from CVE id
    :param cveId: 
    :return: 
    """
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
            the repo, (e.g., ~/diff/dependency_ubuntu)    and use
            one representative CVE that has the smallest ID number
            for filename. 
            A sample:
            CVE-2014-6416_2e9466c84e5beee964e1898dd1f37c3509fa8853    CVE-2014-6418_CVE-2014-6417_CVE-2014-6416_
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
parse_argument()
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
