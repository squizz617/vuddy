#!/usr/bin/env python

import os
import sys

# Import from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import hmark.parseutility as pu

originalDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # vuddy root directory
vulsDir = os.path.join(originalDir, "vul")
dirs = os.listdir(vulsDir)
for dir in dirs:
    for vul in os.listdir(os.path.join(vulsDir, dir)):
        if vul.endswith("OLD.vul"):
            if not vul.endswith(
                    "CVE-2009-0029_7.2_CWE-020_836f92adf121f806e9beb5b6b88bd5c9c4ea3f24_splice.c_33_OLD.vul"):
                continue
            with open(os.path.join('vul', dir, vul), "r") as fp:
                raw = ''.join(fp.readlines())
                body = pu.getBody(pu.removeComment(raw))
            # print body
            cnt = 0
            for line in body.split('\n'):
                if len(line.strip()) > 0:
                    cnt += 1

            with open(os.path.join(vulsDir, dir, vul[:-8] + "_NEW.vul"), 'r') as fp:
                raw = ''.join(fp.readlines())
                newbody = pu.getBody(pu.removeComment(raw))

            print pu.normalize(body)
            print pu.normalize(newbody)
            print "----------------------------------------------"
            if pu.normalize(body) == pu.normalize(newbody):
                print vul

            if cnt == 1:
                vulBase = vul[:-8]
                print vulBase
                print raw
                print "======"
            # os.remove(os.path.join('vul', dir, vulBase + "_OLD.vul"))
            # os.remove(os.path.join('vul', dir, vulBase + "_NEW.vul"))
            # os.remove(os.path.join('vul', dir, vulBase + ".patch"))
