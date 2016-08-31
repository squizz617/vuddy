"""
hidx generator with fixed loc!!
(for tendency graph plotting)
Author: Seulbae Kim
Created: August 31, 2016
"""

import sys
import os
import parseutility
import time
from hashlib import md5

# print "USAGE: python hidxgen.py REPONAME ABSLVL GRANULARITY (f for full-function)"

""" GLOBALS """
try:
	os.mkdir("hidx-retested")
except OSError:
	pass
repoName = "ubuntu"
# saveDir = os.path.join(os.getcwd(), "hidx")
# projDic = {}
# hashFileMap = {}
# absLvl = 0
projInstanceList = []

locList = os.listdir("vul-per-length")
for li, loc in enumerate(locList):
	locList[li] = int(loc)
locList = sorted(locList)
print locList
sys.exit()


""" OFFICIAL """
if len(sys.argv) == 2:
	repoName = sys.argv[1]

print "Processing", repoName

class project:
	repoName = None
	absLvl = None
	granLvl = None
	pid = None
	timeCost = None
	projDic = {}
	hashFileMap = {}

	def __init__(self, repoName, absLvl, granLvl, pid):
		self.repoName = repoName
		self.absLvl = absLvl
		self.granLvl = granLvl
		self.pid = pid
		self.timeCost = 0
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
		with open("hidx-timecost/hashmark_" + str(self.absLvl) + '_' + str(self.granLvl) + '_' + self.repoName + ".hidx", 'w') as fp:
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
		print "Wrote", "hidx/hashmark_" + str(self.absLvl) + '_' + str(self.granLvl) + '_' + self.repoName + ".hidx"

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
# for p in projInstanceList:
	# print p.pid, p.absLvl, p.granLvl
# sys.exit()
vulList = []
for vul in os.listdir("vul/" + repoName):
	if vul.endswith("OLD.vul"):
		vulList.append(vul)

timeCostList = []
for i in range(8):
	timeCostList.append(0)

ioCostList = []
for i in range(8):
	ioCostList.append(0)

for vi, vul in enumerate(vulList):
	print "\t" + str(vi+1) + "/" + str(len(vulList)), vul
	fileName = os.path.join("vul", repoName, vul)
	funcInstance = parseutility.parseFile(fileName)
	for f in funcInstance:
		f.removeListDup()
		path = f.parentFile
		lineList = []

		abstractBodyList = []
		for absLvl in range(5):
			abstractBodyList.append(parseutility.removeComment(parseutility.abstract(f, absLvl)[1]))

		abstractNormalizedBodyLinesList = []	# list of linelist
		for abstractBody in abstractBodyList:
			lineList = []
			for line in abstractBody.split('\n'):
				normLine = parseutility.normalize(line)
				if len(normLine) > 1:
					lineList.append(normLine)
			abstractNormalizedBodyLinesList.append(lineList)

		# for a in abstractNormalizedBodyLinesList:
		# 	print a
		# sys.exit()

		vcnt = 0
		for granLvl in range(4, 11):	# each granularity
			begin = time.time()
			print granLvl,
			for i in range(vcnt, vcnt+5):	# i%5 becomes absLvl from 0 to 4
				absLvl = i%5
				# print "ABST:", absLvl
				lineList = abstractNormalizedBodyLinesList[absLvl-5]
				if len(lineList)-granLvl+1 < 0:
					# print "ABORT"
					continue
				# else:
				# 	print "RANGE:", "0 ~", len(lineList)-granLvl+1

				for lidx in range(0, len(lineList)-granLvl+1):	# each window
					window = lineList[lidx:lidx+granLvl]
					window = ''.join(window)
					# print window
					# window = parseutility.normalize(parseutility.abstractWindow(f, i%5, lineList[lidx:lidx+granLvl])[1])
					# print window
					funcLen = len(window)
					hashValue = md5(window).hexdigest()
					# print funcLen, hashValue
					projInstanceList[(granLvl-4)*5+absLvl].add_to_dictionary(funcLen, hashValue, path, f.funcId)
					# print "PID:", projInstanceList[(granLvl-4)*5+absLvl].pid
					# projInstance
					# print window
					# print projInstance.pid, len(projInstance.projDic)
					# print '\n'
				# print '\n'
			print "%.6f" % (time.time()-begin)
			timeCostList[granLvl-4] += time.time()-begin
			vcnt += 5

		granLvl = "f"
		print granLvl,
		begin = time.time()
		for i in range(vcnt, vcnt+5):
			# print i
			absLvl = i%5
			lineList = abstractNormalizedBodyLinesList[absLvl-5]
			window = ''.join(lineList)
			# window = parseutility.normalize(parseutility.abstract(f, i%5)[1])
			funcLen = len(window)
			hashValue = md5(window).hexdigest()
			projInstanceList[i].add_to_dictionary(funcLen, hashValue, path, f.funcId)
		print "%.6f" % (time.time()-begin)
		timeCostList[7] += time.time()-begin

# i = 0
# for p in projInstanceList:
# 	print p.granLvl,
# 	begin = time.time()
# 	p.write_to_file()
# 	ioCostList[i/5] += time.time()-begin
# 	i += 1
# 	# sys.exit()

# print "Time Cost"
# for t in timeCostList:
# 	print t

# print "I/O Time Cost"
# for t in ioCostList:
# 	print t



		# if granLevel == "f":	# for function-level granularity
		# 	body = parseutility.normalize(parseutility.abstract(f, absLvl)[1])
		# 	funcLen = len(body)
		# 	hashValue = md5(body).hexdigest()

			

		# else:	# for smaller granularity
		# 	granLevel = int(granLevel)
		# 	body = parseutility.getBody(f.getOriginalFunction())
		# 	body = parseutility.removeComment(body)
		# 	# body = body.replace("{", "").replace("}", "")

		# 	for line in body.split('\n'):
		# 		if len(line) > 1:
		# 			lineList.append(line.strip())

		# 	for lidx in range(0, len(lineList)-granLevel+1):
		# 		window = parseutility.normalize(parseutility.abstractWindow(f, absLvl, lineList[lidx:lidx+granLevel])[1])
		# 		funcLen = len(window)
		# 		hashValue = md5(window).hexdigest()

		# 		try:
		# 			projDic[funcLen].append(hashValue)
		# 		except KeyError:
		# 			projDic[funcLen] = [hashValue]

		# 		try:
		# 			hashFileMap[hashValue].extend([path, 1])
		# 		except KeyError:
		# 			hashFileMap[hashValue] = [path, 1]



