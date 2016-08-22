"""
This is a HIDX generator.
Author: Seulbae Kim
Created: August 22, 2016
"""

import sys
import os
import parseutility
from hashlib import md5

print "USAGE: python hidxgen.py REPONAME GRANULARITY (f for full-function)"

""" GLOBALS """
try:
	os.mkdir("hidx")
except OSError:
	pass
saveDir = os.path.join(os.getcwd(), "hidx")
projDic = {}
hashFileMap = {}
absLvl = 0

""" OFFICIAL """
if len(sys.argv) > 2:
	repoName = sys.argv[1]
	granLevel = sys.argv[2]

""" FOR TESTING """
repoName = "ubuntu"
granLevel = "4"

vulList = []
for vul in os.listdir("vul/" + repoName):
	if vul.endswith("OLD.vul"):
		vulList.append(vul)

for vul in vulList:
	fileName = os.path.join("vul", repoName, vul)
	funcInstance = parseutility.parseFile(fileName)
	for f in funcInstance:
		print "Function:", f.name
		print "Path:", f.parentFile
		path = f.parentFile
		lineList = []
		# windowList = []
		if granLevel == "f":
			print parseutility.normalize(parseutility.abstract(f, absLvl)[1])
		else:
			granLevel = int(granLevel)
			body = parseutility.getBody(f.getOriginalFunction())
			body = parseutility.removeComment(body)
			body = body.replace("{", "").replace("}", "")

			print body
			for line in body.split('\n'):
				if len(line) > 1:
					lineList.append(line.strip())

			for lidx in range(0, len(lineList)-granLevel+1):
				# print lidx, lineList[lidx:lidx+granLevel]
				window = parseutility.normalize(parseutility.abstractWindow(f, absLvl, lineList[lidx:lidx+granLevel])[1])
				funcLen = len(window)
				hashValue = md5(window).hexdigest()

				try:
					projDic[funcLen].append(hashValue)
				except KeyError:
					projDic[funcLen] = [hashValue]

				try:
					hashFileMap[hashValue].extend([path, 1])
				except KeyError:
					hashFileMap[hashValue] = [path, 1]

		# print parseutility.getBody(f.getOriginalFunction())
	for key in projDic:
		print key, projDic[key]

	for key in hashFileMap:
		print key, hashFileMap[key]
	# sys.exit()