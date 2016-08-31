"""
This is a experimental version of HIDX generator.
It benchmarks the tradeoff between #LoC & Granularity Level
Author: Seulbae Kim
Created: August 22, 2016
"""

import sys
import os
import parseutility
import time
from hashlib import md5

# print "USAGE: python hidxgen.py REPONAME ABSLVL GRANULARITY (f for full-function)"

""" GLOBALS """
try:
	os.mkdir("hidx-timecost")
except OSError:
	pass
# repoName = "case1-normal"
# repoName = "case2-reverse"
repoName = "case3-arbitrary"
projInstanceList = []

""" OFFICIAL """
if len(sys.argv) == 2:
	repoName = sys.argv[1]

# print "Processing", repoName

class project:
	repoName = None
	absLvl = None
	granLvl = None
	pid = None
	projDic = {}
	hashFileMap = {}

	def __init__(self, repoName, absLvl, granLvl, pid):
		self.repoName = repoName
		self.absLvl = absLvl
		self.granLvl = granLvl
		self.pid = pid
		self.projDic = {}
		self.hashFileMap = {}

	def add_to_dictionary(self, funcLen, hashValue, path, funcId):
		# print "adding", funcLen, hashValue, "to", self.pid
		try:
			self.projDic[funcLen].append(hashValue)
		except KeyError:
			self.projDic[funcLen] = [hashValue]

		try:
			self.hashFileMap[hashValue].extend([path, int(funcId)])
		except KeyError:
			self.hashFileMap[hashValue] = [path, int(funcId)]
		# print self.pid, "has", len(self.projDic)

	def write_to_file(self):
		with open("hidx-timecost-retest/hashmark_" + str(self.absLvl) + '_' + str(self.granLvl) + '_' + self.repoName + ".hidx", 'w') as fp:
			fp.write(self.repoName + '\n')
			for key in sorted(self.projDic):
				fp.write(str(key) + '\t')
				for h in list(set(self.projDic[key])):
					fp.write(h + '\t')
				fp.write('\n')
				
			fp.write('\n=====\n')

			for key in sorted(self.hashFileMap):
				fp.write(str(key) + '\t')
				for f in self.hashFileMap[key]:
					fp.write(str(f) + '\t')
				fp.write('\n')
		# print "Wrote", "hidx/hashmark_" + str(self.absLvl) + '_' + str(self.granLvl) + '_' + self.repoName + ".hidx"

pid = 0
for granLvl in range(4, 11):
	for absLvl in range(0, 5):
		projInstance = project(repoName, absLvl, granLvl, pid)
		projInstanceList.append(projInstance)
		pid += 1
for absLvl in range(0, 5):
	projInstance = project(repoName, absLvl, "f", pid)
	projInstanceList.append(projInstance)
	pid += 1
# print "REPO:", repoName, "ABS:", absLvl, "GRAN:", granLevel
for p in projInstanceList:
	print p.pid, p.absLvl, p.granLvl
# sys.exit()

vulList = []
for vul in os.listdir(repoName):
	if vul.endswith("OLD.vul"):
		vulList.append(vul)

# timeCostList = []
# for i in range(8):
# 	timeCostList.append(0)

# ioCostList = []
# for i in range(8):
# 	ioCostList.append(0)

maxTrials = 100
trial = 0

#	G: [Parse, AbsNor, Hash, Store, IO, Total]
#	X: GRANLVL / Y: ITEM / Z: ABSLVL
resultDict = {
	4: [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
	5: [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
	6: [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
	7: [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
	8: [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
	9: [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
	10: [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
	"f": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
}


vul = vulList[0]
# t0 = time.time()
fileName = os.path.join(repoName, vul)
funcInstance = parseutility.parseFile(fileName)
# time_parse = time.time() - t0
f = funcInstance[0]
f.removeListDup()
path = f.parentFile
abstractBodyList = [
		parseutility.abstract(f, 0)[1],
		parseutility.abstract(f, 1)[1],
		parseutility.abstract(f, 2)[1],
		parseutility.abstract(f, 3)[1],
		parseutility.abstract(f, 4)[1]
	]
abstractBody = parseutility.abstract(f, 0)[1]
for absLvl in range(5):
	abstractBody = abstractBodyList[absLvl]
	abstractBodyList[absLvl] = parseutility.removeComment(abstractBody)

# print abstractBodyList
# for ab in abstractBodyList:
# 	print ab
# 	print parseutility.removeComment(ab)

for absLvl in range(5):
	print "ABSTRACTION LEVEL-" + str(absLvl)
	lineList = []

	abstractBody = abstractBodyList[absLvl]
	print abstractBody
	for line in abstractBody.split('\n'):
		normLine = parseutility.normalize(line)
		if len(normLine) > 1:
			lineList.append(normLine)

	print lineList
	print len(lineList), "LINES"

	fp = open("RESULTS-retest/" + str(absLvl) + '_' + str(len(lineList)), "w")
	while trial < maxTrials:
		vcnt = 0
		for granLvl in range(4, 11):	# each granularity
			for lidx in range(0, len(lineList)-granLvl+1):	# each window
				# for i in range(vcnt, vcnt+5):	# i%5 becomes absLvl from 0 to 4
				t1 = time.time()
				window = ''.join(lineList[lidx:lidx+granLvl])
				# print window
				# sys.exit()
				# window = parseutility.normalize(parseutility.abstractWindow(f, i%5, lineList[lidx:lidx+granLvl])[1])
				resultDict[granLvl][0][absLvl] += time.time()-t1

				t2 = time.time()
				funcLen = len(window)
				hashValue = md5(window).hexdigest()
				resultDict[granLvl][1][absLvl] += time.time()-t2

				t3 = time.time()
				projInstanceList[5*(granLvl-4)+absLvl].add_to_dictionary(funcLen, hashValue, path, f.funcId)
				resultDict[granLvl][2][absLvl] += time.time()-t3

			# vcnt += 5

		granLvl = "f"
		# for i in range(vcnt, vcnt+5):
		t1 = time.time()
		window = ''.join(lineList)
		print window
		# window = parseutility.normalize(parseutility.abstract(f, i%5)[1])
		resultDict[granLvl][0][absLvl] += time.time()-t1

		t2 = time.time()
		funcLen = len(window)
		hashValue = md5(window).hexdigest()
		resultDict[granLvl][1][absLvl] += time.time()-t2

		t3 = time.time()
		projInstanceList[i].add_to_dictionary(funcLen, hashValue, path, f.funcId)
		resultDict[granLvl][2][absLvl] += time.time()-t3

		i = 0
		for p in projInstanceList:
			print p
			print type(p.absLvl), type(absLvl)
			if p.absLvl == absLvl:
				begin = time.time()
				p.write_to_file()
				time_IO = time.time() - begin
				if p.granLvl != "f":
					resultDict[i/5+4][3][absLvl] += time_IO
				else:
					resultDict["f"][3][absLvl] += time_IO
				i += 1

		trial += 1

	for granLvl in resultDict:	# calculate total time
		for i in range(5):
			resultDict[granLvl][4][absLvl] += resultDict[granLvl][i][absLvl]

	fp.write("Gra\tAbs&Norm\tHashComp\tStoreInDict\tDisk I/O\tTotal\n")
	for granLvl in resultDict:
		fp.write("%s\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\n" %\
			(
				granLvl,
				resultDict[granLvl][0][absLvl]/maxTrials,
				resultDict[granLvl][1][absLvl]/maxTrials,
				resultDict[granLvl][2][absLvl]/maxTrials,
				resultDict[granLvl][3][absLvl]/maxTrials,
				resultDict[granLvl][4][absLvl]/maxTrials
			)
		)
		# granLvl, resultDict[granLvl]
	fp.close()

# print "%d\t%.6f\t%.6f\t%.6f\t%.6f" % (granLvl, time_parse, time_hash, time_store, time.time()-begin)

