import os
import sys
import pickle

import parseutility as p

mapDict = pickle.load(open("cvedata.pkl", "rb"))

cveDict = {}
c = 0
dirs = os.listdir('vul')
for d in dirs:
	path = "vul/" + d
	files = os.listdir(path)
	for f in files:
		if f.endswith('OLD.vul'):
			cve = f.split('_')[0]
			try:
				cveDict[cve] += 1
			except:
				cveDict[cve] = 1

files = os.listdir('diff')
for f in files:
	if f.startswith("dependency_"):
		with open("diff/" + f, "r") as fp:
			lines = fp.readlines()
		for line in lines:
			cveList = line.split('\t')[1].split('_')[:-1]
			for cve in cveList:
				try:
					cveDict[cve] += 1
				except:
					cveDict[cve] = 1

print len(cveDict)

yearDict = {}

cweDict = {}


for cve in cveDict:
	try:
		cwe = mapDict[cve][1]
		if cwe in cweDict:
			cweDict[cwe] += 1
		else:
			cweDict[cwe] = 1
	except:
		pass

	year = cve.split('-')[1]
	if year in yearDict:
		yearDict[year] += 1
	else:
		yearDict[year] = 1

print len(cweDict)

yearKeys = yearDict.keys()
for year in sorted(yearKeys):
	print year, yearDict[year]

cweKeys = cweDict.keys()
for cwe in sorted(cweKeys):
	print cwe + '\t' + str(cweDict[cwe])
