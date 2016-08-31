import parseutility
import os
import sys
import hashlib

targetDir = "/home/squizz/Downloads/SM-G930S-G930SKSU1APB2/Kernel"
path = "SM-G930S-G930SKSU1APB2/"
projName = "S7"
granLvl = "f"

projDictList = []
hashFileMapList = []
for i in range(0, 5):
	projDictList.append({})
	hashFileMapList.append({})

print "loading source",
srcFileList = parseutility.loadSource(targetDir)
print "(done)"

for si, srcFile in enumerate(srcFileList):
	print si+1, '/', len(srcFileList), srcFile
	functionInstanceList = parseutility.parseFile(srcFile)

	for f in functionInstanceList:
		f.removeListDup()
		for absLvl in range(0, 5):
			window = parseutility.normalize(parseutility.abstract(f, absLvl)[1])
			funcLen = len(window)
			hashValue = hashlib.md5(window).hexdigest()

			try:
				projDictList[absLvl][funcLen].append(hashValue)
			except KeyError:
				projDictList[absLvl][funcLen] = [hashValue]

			try:
				hashFileMapList[absLvl][hashValue].extend([f.parentFile, f.funcId])
			except KeyError:
				hashFileMapList[absLvl][hashValue] = [f.parentFile, f.funcId]

for i in range(0, 5):
	with open("hidx-target/hashmark_" + str(i) + '_' + "f" + '_' + projName + ".hidx", 'w') as fp:
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
