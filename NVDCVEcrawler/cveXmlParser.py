"""
NVD's CVE xml data processor.
xml data is downloaded from https://nvd.nist.gov/download.cfm
This module should be run only one time.
or, if the pickle file has been corrupted, run this module again.
Updates of the database is done in cvexmlupdater.py
"""

import os
import pickle
import common

DLDir = "CVEXML"
cveDict = {}
reference = []

pwd = os.getcwd()
os.chdir(DLDir)

for xml in os.listdir("."):
	subDict = common.parse_xml(xml)
	cveDict.update(subDict)

os.chdir(pwd)
pickle.dump(cveDict, open("cvedata.pkl", "wb"))

print "Stored " + str(len(cveDict)) + " CVE data in file 'cvedata.pkl'."