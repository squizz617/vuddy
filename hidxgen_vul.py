import parseutility
import os
import sys
import hashlib
import time

projName = "android"
intendedGranLvl = 'f'
intendedAbsLvl = 4
projDictList = []
hashFileMapList = []
for i in range(0, 5):
	projDictList.append({})
	hashFileMapList.append({})

print "loading source",
srcFileList = parseutility.loadVul("./vul/" + projName)
print "(done)"

time0 = time.time()

numFiles = len(srcFileList)
numFuncs = 0
numLines = 0

for si, srcFile in enumerate(srcFileList):
	print si+1, '/', len(srcFileList), srcFile
	functionInstanceList = parseutility.parseFile(srcFile)
	
	numFuncs += len(functionInstanceList)
	if len(functionInstanceList) > 0:
		numLines += functionInstanceList[0].parentNumLoc

	for f in functionInstanceList:
		f.removeListDup()
		path = f.parentFile
		absBody = parseutility.abstract(f, intendedAbsLvl)[1]
		absBody = parseutility.normalize(absBody)
		funcLen = len(absBody)
		hashValue = hashlib.md5(absBody).hexdigest()

		try:
			projDictList[intendedAbsLvl][funcLen].append(hashValue)
		except KeyError:
			projDictList[intendedAbsLvl][funcLen] = [hashValue]

		try:
			hashFileMapList[intendedAbsLvl][hashValue].extend([f.parentFile, f.funcId])
		except KeyError:
			hashFileMapList[intendedAbsLvl][hashValue] = [f.parentFile, f.funcId]

for i in range(0, 5):
	if i == intendedAbsLvl:
		packageInfo = str(projName) + ' ' + str(numFiles) + ' ' + str(numFuncs) + ' ' + str(numLines) + '\n'
		with open("hidx-vul/hashmark_" + str(i) + '_' + str(intendedGranLvl) + '_' + projName + ".hidx", 'w') as fp:
			fp.write(packageInfo)
			for key in sorted(projDictList[i]):
				fp.write(str(key) + '\t')
				for h in list(set(projDictList[i][key])):
					fp.write(h + '\t')
				fp.write('\n')
			
			fp.write('\n=====\n')

			for key in sorted(hashFileMapList[i]):
				fp.write(str(key) + '\t')
				for f in hashFileMapList[i][key]:
					fp.write(str(f) + '\t')
				fp.write('\n')


time1 = time.time()
print "Elapsed time:", time1 - time0