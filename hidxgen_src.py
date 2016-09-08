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
projDictList = []
hashFileMapList = []
for i in range(0, 5):
	projDictList.append({})
	hashFileMapList.append({})

print "loading source",
srcFileList = parseutility.loadSource(targetDir)
print "(done)"

locList = os.listdir("vul-per-length")
for li, loc in enumerate(locList):
	locList[li] = int(loc)
locList = sorted(locList)

time0 = time.time()

numFiles = len(srcFileList)
numFuncs = 0
numLines = 0

if intendedGranLvl == 'f':
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
				projDictList[intendedAbsLvl][funcLen].append(hashValue)
			except KeyError:
				projDictList[intendedAbsLvl][funcLen] = [hashValue]

			try:
				hashFileMapList[intendedAbsLvl][hashValue].extend([f.parentFile, f.funcId])
			except KeyError:
				hashFileMapList[intendedAbsLvl][hashValue] = [f.parentFile, f.funcId]

	for i in range(0, 5):
		if i == intendedAbsLvl:
			with open("hidx-target/hashmark_" + str(i) + '_' + str(intendedGranLvl) + '_' + projName + ".hidx", 'w') as fp:
				fp.write(projName + '\n')
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

else:
	for granLvl in locList:
		if granLvl != intendedGranLvl:
			continue
		for si, srcFile in enumerate(srcFileList):
			print si+1, '/', len(srcFileList), srcFile
			functionInstanceList = parseutility.parseFile(srcFile)

			for f in functionInstanceList:
				f.removeListDup()
				path = f.parentFile
				absBody = parseutility.abstract(f, intendedAbsLvl)[1]
				lineList = []
				for line in absBody.split('\n'):
					normLine = parseutility.normalize(line)
					if len(normLine) > 1:
						lineList.append(normLine)

				for lidx in range(0, len(lineList)-granLvl+1):
					window = ''.join(lineList[lidx:lidx+granLvl])
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
				with open("hidx-target/hashmark_" + str(i) + '_' + str(granLvl) + '_' + projName + ".hidx", 'w') as fp:
					fp.write(projName + '\n')
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