"""
CVE data updater.
Run cveXmlDownloader.py and cveXmlParser.py before running this module.
This module downloads "modified" data from NVD, uncompress and update the database.
"""

import os
import pickle
import common

# first download the modified cve data from NVD
fileName = "nvdcve-2.0-modified.xml.zip"
url = "http://static.nvd.nist.gov/feeds/xml/cve/" + fileName

common.download_url(url, fileName)
common.unzip(fileName)
os.remove(fileName)

# load the pickled cve data
print "Reading pickled data...",
cveDict = pickle.load(open("cvedata.pkl", "rb"))
print "[DONE]"

reference = []

update_count = 0
new_count = 0

subDict = common.parse_xml(fileName.replace(".zip", ""))
cveDict.update(subDict)

# print "Updated %s records, added %s records." % (update_count, new_count)

print "Dumping updated pickle...",
pickle.dump(cveDict, open("cvedata.pkl", "wb"))
os.remove(fileName.replace(".zip", ""))
print "[DONE]"
