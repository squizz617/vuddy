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
originalDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def process():
    DLDir = os.path.join(originalDir, "data", "CVEXML")
    cveDict = {}

    for xml in os.listdir(DLDir):
        subDict = common.parse_xml(os.path.join(DLDir, xml))
        cveDict.update(subDict)

    pickle.dump(cveDict, open(os.path.join(originalDir, "data", "cvedata.pkl"), "wb"))

    print "Stored " + str(len(cveDict)) + " CVE data in file 'cvedata.pkl'."


if __name__ == '__main__':
    process()
