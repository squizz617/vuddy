import os
import sys
import argparse
import urllib2
import json
import logging

logging.basicConfig(filename='repo_updater.log', level=logging.WARNING)

parser = argparse.ArgumentParser()
parser.add_argument('REPO',
                    help='''Repository name''')

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
    print ri+1, "/", len(repo_list), "\t", target_dir,
    if os.path.isdir(target_dir):
        print "exists. PULL"
        os.chdir(target_dir)
        os.system("git pull")
        os.chdir(cwd)
    else:
        print "NULL. CLONE."
        os.system("git clone {0}{1} {2}".format(url_base, repo, target_dir))
    

