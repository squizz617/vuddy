import parseutility
import os
import sys
import hashlib
import time

targetDir = "/home/squizz/Downloads/SM-G930S-G930SKSU1APB2/Kernel"
path = "SM-G930S-G930SKSU1APB2/"
projName = "S7"
intendedGranLvl = 'f'
intendedAbsLvl = int(raw_input("Abstraction Level? "))

projDict = {}
hashFileMap = {}

print "loading source",
srcFileList = parseutility.loadSource(targetDir)
print "(done)"

time0 = time.time()

numFiles = len(srcFileList)
numFuncs = 0
numLines = 0

for si, srcFile in enumerate(srcFileList):
	print si+1, '/', len(srcFileList), srcFile
	functionInstanceList = parseutility.parseFile(srcFile)

	numFuncs += len(functionInstanceList)

	for f in functionInstanceList:
		f.removeListDup()
		numLines += f.parentNumLoc
		path = f.parentFile
		absBody = parseutility.abstract(f, intendedAbsLvl)[1]
		absBody = parseutility.normalize(absBody)
		funcLen = len(absBody)
		hashValue = hashlib.md5(absBody).hexdigest()

		try:
			projDict[funcLen].append(hashValue)
		except KeyError:
			projDict[funcLen] = [hashValue]

		try:
			hashFileMap[hashValue].extend([f.parentFile, f.funcId])
		except KeyError:
			hashFileMap[hashValue] = [f.parentFile, f.funcId]

packageInfo = str(projName) + ' ' + str(numFiles) + ' ' + str(numFuncs) + ' ' + str(numLines) + '\n'
with open("hidx-target/hashmark_" + str(intendedAbsLvl) + '_' + str(intendedGranLvl) + '_' + projName + ".hidx", 'w') as fp:
	fp.write(packageInfo)
	for key in sorted(projDict):
		fp.write(str(key) + '\t')
		for h in list(set(projDict[key])):
			fp.write(h + '\t')
		fp.write('\n')
	
	fp.write('\n=====\n')

	for key in sorted(hashFileMap):
		fp.write(str(key) + '\t')
		for f in hashFileMap[key]:
			fp.write(str(f) + '\t')
		fp.write('\n')

time1 = time.time()
print "Elapsed time:", time1 - time0