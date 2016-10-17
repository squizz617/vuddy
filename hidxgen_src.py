import parseutility
import os
import sys
import hashlib
import time

import TreeParser

targetDir = "/home/squizz/Desktop/ffmpeg-2.8.6"
projName = "ffmpeg-2.8.6"
intendedGranLvl = raw_input("Granularity level? ")
if intendedGranLvl != 'f':
	intendedGranLvl = int(intendedGranLvl)
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

if intendedGranLvl == 'f':
	for si, srcFile in enumerate(srcFileList):
		print si+1, '/', len(srcFileList), srcFile
		
		# functionInstanceList = TreeParser.TreeParser().parseFile(srcFile)
		functionInstanceList = parseutility.parseFile(srcFile)

		numFuncs += len(functionInstanceList)

		if len(functionInstanceList) > 0:	# we shouldn't count multiple times
			numLines += functionInstanceList[0].parentNumLoc

		for f in functionInstanceList:
			f.removeListDup()
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
else:
	for si, srcFile in enumerate(srcFileList):
		print si+1, '/', len(srcFileList), srcFile
		functionInstanceList = TreeParser.parseFile(srcFile)

		numFuncs += len(functionInstanceList)

		if len(functionInstanceList) > 0:	# we shouldn't count multiple times
			numLines += functionInstanceList[0].parentNumLoc

		for f in functionInstanceList:
			f.removeListDup()
			path = f.parentFile
			absBody = parseutility.abstract(f, intendedAbsLvl)[1]
			lineList = []
			for line in absBody.split('\n'):
				normLine = parseutility.normalize(line)
				if len(normLine) > 1:
					lineList.append(normLine)

			for lidx in range(0, len(lineList)-intendedGranLvl+1):
					window = ''.join(lineList[lidx:lidx+intendedGranLvl])
					funcLen = len(window)
					hashValue = hashlib.md5(window).hexdigest()

					try:
						projDict[funcLen].append(hashValue)
					except KeyError:
						projDict[funcLen] = [hashValue]

					try:
						hashFileMap[hashValue].extend([f.parentFile, f.funcId])
					except KeyError:
						hashFileMap[hashValue] = [f.parentFile, f.funcId]

packageInfo = str(projName) + ' ' + str(numFiles) + ' ' + str(numFuncs) + ' ' + str(numLines) + '\n'
with open("hidx-target-tp/hashmark_" + str(intendedAbsLvl) + '_' + str(intendedGranLvl) + '_' + projName + ".hidx", 'w') as fp:
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
