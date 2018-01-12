import os
import sys
import argparse
import urllib2
import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler = logging.FileHandler("repo_updater.log")
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

parser = argparse.ArgumentParser()
parser.add_argument('REPO', help='''Repository name''')

args = parser.parse_args()

if args.REPO is None:
    parser.print_help()
    exit()

cwd = os.getcwd()
repo_name = args.REPO
git_dir = "/home/whiteboxDB/gitrepos"

if repo_name.lower() == "android":
    url_base = "https://android.googlesource.com/"
    url_list = url_base + "?format=TEXT"
    response = urllib2.urlopen(url_list)
    repo_list = response.read().rstrip().split("\n")
    repo_base = os.path.join(git_dir, repo_name) 
elif repo_name.lower() == "chromium":
    url_base = "https://chromium.googlesource.com/"
    url_list = url_base + "?format=TEXT"
    response = urllib2.urlopen(url_list)
    repo_list = response.read().rstrip().split("\n")
    repo_base = os.path.join(git_dir, repo_name)

if not os.path.isdir(repo_base):
    os.mkdir(repo_base)

for ri, repo in enumerate(repo_list):
    target_dir = os.path.join(repo_base, repo)
    infostr = str(ri+1) + "/" + str(len(repo_list)) + "\t" + repo
    if os.path.isdir(target_dir):
        infostr += " EXISTS (PULL)"
        logger.info(infostr)
        os.chdir(target_dir)
        os.system("git pull")
        os.chdir(cwd)
    else:
        infostr += " DOESN'T EXIST (CLONE)"
        logger.info(infostr)
        os.system("git clone {0}{1} {2}".format(url_base, repo, target_dir))
    

