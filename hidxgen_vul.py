import parseutility
import os
import sys
import hashlib
import time

if len(sys.argv) == 1:
	projName = "codeaurora"
	intendedAbsLvl = 4
	intendedGranLvl = 4
else:
	projName = sys.argv[1]
	intendedAbsLvl = int(sys.argv[2])
	intendedGranLvl = sys.argv[3]

if intendedGranLvl != 'f':
	intendedGranLvl = int(intendedGranLvl)

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

if intendedGranLvl == 'f':
	for si, srcFile in enumerate(srcFileList):
		print si+1, '/', len(srcFileList), srcFile
		if intendedAbsLvl == 0:
			functionInstanceList = parseutility.parseFile_shallow(srcFile)
		elif intendedAbsLvl == 4:
			functionInstanceList = parseutility.parseFile_deep(srcFile)
			# Some lines below are added by Squizz on Jan 16, for FP reduction!
			functionInstanceList_New = parseutility.parseFile_deep(srcFile.replace("OLD.vul", "NEW.vul"))

		numFuncs += len(functionInstanceList)
		if len(functionInstanceList) > 0:
			numLines += functionInstanceList[0].parentNumLoc

		for fi, f in enumerate(functionInstanceList):
			f.removeListDup()
			path = f.parentFile
			absBody = parseutility.abstract(f, intendedAbsLvl)[1]
			absBody = parseutility.normalize(absBody)
			funcLen = len(absBody)
			hashValue = hashlib.md5(absBody).hexdigest()

			if intendedAbsLvl == 4 and len(functionInstanceList_New) > 0:
				fnew = functionInstanceList_New[fi]
				fnew.removeListDup()
				absBodyNew = parseutility.abstract(fnew, intendedAbsLvl)[1]
				absBodyNew = parseutility.normalize(absBodyNew)
				hashValueNew = hashlib.md5(absBodyNew).hexdigest()

				if hashValue == hashValueNew:
					# if abstract bodies of old and new func are identical,
					# don't create hash index
					continue

			try:
				projDictList[intendedAbsLvl][funcLen].append(hashValue)
			except KeyError:
				projDictList[intendedAbsLvl][funcLen] = [hashValue]

			try:
				hashFileMapList[intendedAbsLvl][hashValue].extend([f.parentFile, f.funcId])
			except KeyError:
				hashFileMapList[intendedAbsLvl][hashValue] = [f.parentFile, f.funcId]
else:
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
					projDictList[intendedAbsLvl][funcLen].append(hashValue)
				except KeyError:
					projDictList[intendedAbsLvl][funcLen] = [hashValue]

				try:
					hashFileMapList[intendedAbsLvl][hashValue].extend([f.parentFile, f.funcId])
				except KeyError:
					hashFileMapList[intendedAbsLvl][hashValue] = [f.parentFile, f.funcId]



for i in range(0, 5):
	if i == intendedAbsLvl:
		packageInfo = str("3.0.1") + ' ' + str(projName) + ' ' + str(numFiles) + ' ' + str(numFuncs) + ' ' + str(numLines) + '\n'
		with open("hidx-vul/hashmark_" + str(i) + '_' + projName + ".hidx", 'w') as fp:
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