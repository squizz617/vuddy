#!/usr/bin/env python
"""
NVD's CVE xml data processor.
xml data is downloaded from https://nvd.nist.gov/download.cfm
This module should be run only once.
or, if the pickle file has been corrupted, run this module again.
Updates of the database is done in cvexmlupdater.py
"""

import os
import common
try:
    import cPickle as pickle
except ImportError:
    import pickle


def process():
    DLDir = "CVEXML"
    cveDict = {}
    reference = []

    pwd = os.getcwd()
    print pwd
    os.chdir(DLDir)

    for xml in os.listdir("."):
        subDict = common.parse_xml(xml)
        cveDict.update(subDict)

    os.chdir(pwd)
    pickle.dump(cveDict, open("cvedata.pkl", "wb"))

    print "Stored " + str(len(cveDict)) + " CVE data in file 'cvedata.pkl'."


if __name__ == '__main__':
    process()
