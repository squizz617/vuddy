import os
import sys
import parseutility as p

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