#!/usr/bin/env python
"""
CVE data updater.
Run cveXmlDownloader.py and cveXmlParser.py before running this module.
This module downloads "modified" data from NVD, uncompress and update the database.
"""

import os
import pickle
import common

originalDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def process():
    # first download the modified cve data from NVD
    fileName = "nvdcve-1.1-modified.json.zip"
    url = "https://nvd.nist.gov/feeds/json/cve/1.1/" + fileName

    common.download_url(url, fileName)
    common.unzip(fileName)
    os.remove(fileName)

    # load the pickled cve data
    print "Reading pickled data...",
    cveDict = pickle.load(open(os.path.join(originalDir, "data", "cvedata.pkl"), "rb"))
    print "[DONE]"

    subDict = common.parse_xml(fileName.replace(".zip", ""))
    cveDict.update(subDict)

    os.remove(fileName.replace(".zip", ""))

    print "Dumping updated pickle...",
    pickle.dump(cveDict, open(os.path.join(originalDir, "data", "cvedata.pkl"), "wb"))
    print "[DONE]"


if __name__ == '__main__':
    process()
