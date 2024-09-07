#!/usr/bin/env python

import os
import subprocess
import re
import time
import argparse
import sys
import platform
import multiprocessing as mp
from functools import partial

try:
    import cPickle as pickle
except ImportError:
    import pickle

# Import from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class InfoStruct:
    RepoName = ''  # repository name
    OriginalDir = ''  # vuddy root directory
    DiffDir = ''
    MultimodeFlag = 0
    MultiRepoList = []
    GitBinary = config.gitBinary
    GitStoragePath = config.gitStoragePath
    CveDict = {}
    keyword = "CVE-20"
    cveID = None 
    DebugMode = False

    def __init__(self, originalDir, CveDataPath):
        self.OriginalDir = originalDir
        self.DiffDir = os.path.join(originalDir, 'diff')
        with open(CveDataPath, "rb") as f:
            self.CveDict = pickle.load(f)


""" GLOBALS """
originalDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # vuddy root directory
cveDataPath = os.path.join(originalDir, "data", "cvedata.pkl")
info = InfoStruct(originalDir, cveDataPath)  # first three arg is dummy for now
printLock = mp.Lock()


""" FUNCTIONS """
def parse_argument():
    global info

    parser = argparse.ArgumentParser(prog='get_cvepatch_from_git.py')
    parser.add_argument('REPO',
                        help='''Repository name''')
    parser.add_argument('-m', '--multimode', action="store_true",
                        help='''Turn on Multimode''')
    parser.add_argument('-k', '--keyword',
                        help="Keyword to GREP, default: CVE-20", default="CVE-20")
    parser.add_argument('-c', '--cveid', help="CVE id to assign (Only when doing manual keyword search)")
    parser.add_argument('-d', '--debug', action="store_true", help=argparse.SUPPRESS)  # Hidden Debug Mode
 
    args = parser.parse_args()

    info.RepoName = args.REPO
    info.keyword = args.keyword
    info.cveID = args.cveid
    info.MultimodeFlag = 0
    info.MultiRepoList = []
    if args.multimode:
        info.MultimodeFlag = 1
        if "Windows" in platform.platform():
            with open(os.path.join(originalDir, 'data', 'repolists', 'list_' + info.RepoName)) as fp:
                for repoLine in fp.readlines():
                    if len(repoLine) > 2:
                        info.MultiRepoList.append(repoLine.rstrip())
        else:
            repoBaseDir = os.path.join(info.GitStoragePath, info.RepoName)
            command_find = "find " + repoBaseDir + " -type d -exec test -e '{}/.git' ';' -print -prune"
            findOutput = subprocess.check_output(command_find, shell=True)
            info.MultiRepoList = findOutput.replace(repoBaseDir + "/", "").rstrip().split("\n")
    if args.debug:
        info.DebugMode = True


def init():
    global info

    parse_argument()

    print("Retrieving CVE patch from", info.RepoName)
    print("Multi-repo mode:"),
    if info.MultimodeFlag:
        print("ON.")
    else:
        print("OFF.")

    print("Initializing..."),

    try:
        os.makedirs(os.path.join(info.DiffDir, info.RepoName))
    except OSError:
        pass

    print("Done.")


def callGitLog(gitDir):
    global info
    """
    Collect CVE commit log from repository
    :param gitDir: repository path
    :return:
    """
    # print "Calling git log...",
    commitsList = []
    gitLogOutput = ""
    command_log = "\"{0}\" --no-pager log --all --pretty=fuller --grep=\"{1}\"".format(info.GitBinary, info.keyword)
    print(gitDir)
    os.chdir(gitDir)
    try:
        try:
            gitLogOutput = subprocess.check_output(command_log, shell=True)
            #commitsList = re.split('[\n](?=commit\s\w{40}\nAuthor:\s)|[\n](?=commit\s\w{40}\nMerge:\s)', gitLogOutput)
            commitsList = re.split(b'[\n](?=commit\s\w{40}\nAuthor:\s)|[\n](?=commit\s\w{40}\nMerge:\s)', gitLogOutput)
        except subprocess.CalledProcessError as e:
            print("[-] Git log error:", e)
    except UnicodeDecodeError as err:
        print("[-] Unicode error:", err)

    # print "Done."
    return commitsList


def filterCommitMessage(commitMessage):
    #추가
    commitMessage = commitMessage.decode('utf-8')
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


def callGitShow(gitBinary, commitHashValue):
    """
    Grep data of git show
    :param commitHashValue: 
    :return: 
    """
    # print "Calling git show...",
    command_show = "\"{0}\" show --pretty=fuller {1}".format(gitBinary, commitHashValue)

    gitShowOutput = ''
    try:
        gitShowOutput = subprocess.check_output(command_show, shell=True)
    except subprocess.CalledProcessError as e:
        print("error:", e)

    # print "Done."
    return gitShowOutput


def updateCveInfo(cveDict, cveId):
    """
    Get CVSS score and CWE id from CVE id
    :param cveId: 
    :return: 
    """
    # print "Updating CVE metadata...",
    cvss = "0.0"
    try:
        cvss = str(cveDict[cveId][0])
    except:
        cvss = "0.0"

    cwe = "CWE-000"
    try:
        cwe = cveDict[cveId][1]
    except:
        cwe = "CWE-000"
    if "NVD-CWE-noinfo" in cwe:
        cwe = "CWE-000"
    else:
        cweNum = cwe.split('-')[1].zfill(3)
        cwe = "CWE-" + str(cweNum)

    # print "Done."
    return cveId + '_' + cvss + '_' + cwe + '_'


def process(commitsList, subRepoName):
    global info

    flag = 0
    if len(commitsList) > 0 and commitsList[0] == '':
        flag = 1
        print("No commit in", info.RepoName),
    else:
        print(len(commitsList), "commits in", info.RepoName),
    if subRepoName is None:
        print("\n")
    else:
        print(subRepoName)
        os.chdir(os.path.join(info.GitStoragePath, info.RepoName, subRepoName))

    if flag:
        return

    if info.DebugMode or "Windows" in platform.platform():
        # Windows - do not use multiprocessing
        # Using multiprocessing will lower performance
        for commitMessage in commitsList:
            parallel_process(subRepoName, commitMessage)
    else:  # POSIX - use multiprocessing
        pool = mp.Pool()
        parallel_partial = partial(parallel_process, subRepoName)
        pool.map(parallel_partial, commitsList)
        pool.close()
        pool.join()


def parallel_process(subRepoName, commitMessage):
    global info
    global printLock

    if filterCommitMessage(commitMessage):
        return
    else:
        commitHashValue = commitMessage[7:47]
        # 바이트 문자열인 경우 UTF-8로 변환
        if isinstance(commitHashValue, bytes):
            commitHashValue = commitHashValue.decode('utf-8')
        #추가
        commitMessage = commitMessage.decode('utf-8')
        cvePattern = re.compile('CVE-20\d{2}-\d{4,7}')  # note: CVE id can now be 7 digit numbers
        cveIdList = list(set(cvePattern.findall(commitMessage)))
        
        """    
        Note: Aug 5, 2016
        If multiple CVE ids are assigned to one commit,
        store the dependency in a file which is named after
        the repo, (e.g., ~/diff/dependency_ubuntu)    and use
        one representative CVE that has the smallest ID number
        for filename. 
        A sample:
        CVE-2014-6416_2e9466c84e5beee964e1898dd1f37c3509fa8853    CVE-2014-6418_CVE-2014-6417_CVE-2014-6416_
        """

        if len(cveIdList) > 1:  # do this only if muliple CVEs are assigned to a commit
            dependency = os.path.join(info.DiffDir, "dependency_" + info.RepoName)
            with open(dependency, "a") as fp:
                cveIdFull = ""
                minCve = ""
                minimum = 9999999
                for cveId in cveIdList:
                    idDigits = int(cveId.split('-')[2])
                    cveIdFull += cveId + '_'
                    if minimum > idDigits:
                        minimum = idDigits
                        minCve = cveId
                #세 줄 추가
                minCve = minCve.decode('utf-8') if isinstance(minCve, bytes) else minCve
                cveIdFull = cveIdFull.decode('utf-8') if isinstance(cveIdFull, bytes) else cveIdFull
                fp.write(str(minCve + '_' + commitHashValue + '\t' + cveIdFull + '\n'))
        elif len(cveIdList) == 0:
            if info.cveID is None:
                return
            else:
                minCve = info.cveID  # when CVE ID is given manually through command line argument
        else:
            minCve = cveIdList[0]

        #추가
        #git_command = f"git show --pretty=fuller {commitHashValue}"
        gitShowOutput = callGitShow(info.GitBinary, commitHashValue)
        # gitShowOutput이 바이트 문자열인 경우 문자열로 변환
        if isinstance(gitShowOutput, bytes):
            gitShowOutput = gitShowOutput.decode('latin-1') # latin-1 만 가능

        finalFileName = updateCveInfo(info.CveDict, minCve)

        diffFileName = "{0}{1}.diff".format(finalFileName, commitHashValue)
        try:
            #with open(os.path.join(info.DiffDir, info.RepoName, diffFileName), "w") as fp:
            with open(os.path.join(info.DiffDir, info.RepoName, diffFileName), "w", encoding="utf-8") as fp:
                if subRepoName is None:
                    fp.write(gitShowOutput)
                else:  # multi-repo mode
                    fp.write(subRepoName + '\n' + gitShowOutput)
            with printLock:
                print("[+] Writing {0} Done.".format(diffFileName))
        except IOError as e:
            with printLock:
                print("[+] Writing {0} Error:".format(diffFileName), e)


def main():
    global info

    t1 = time.time()
    init()
    if info.MultimodeFlag:
        for sidx, subRepoName in enumerate(info.MultiRepoList):
            gitDir = os.path.join(info.GitStoragePath, info.RepoName, subRepoName)  # where .git exists
            commitsList = callGitLog(gitDir)
            print(os.path.join(str(sidx + 1), str(len(info.MultiRepoList))))
            if 0 < len(commitsList):
                process(commitsList, subRepoName)
    else:
        gitDir = os.path.join(info.GitStoragePath, info.RepoName)  # where .git exists
        commitsList = callGitLog(gitDir)
        process(commitsList, None)

    repoDiffDir = os.path.join(info.DiffDir, info.RepoName)
    print(str(len(os.listdir(repoDiffDir))) + " patches saved in", repoDiffDir)
    print("Done. (" + str(time.time() - t1) + " sec)")


if __name__ == '__main__':
    mp.freeze_support()
    main()
