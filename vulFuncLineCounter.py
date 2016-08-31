import os
import sys
import parseutility as p

linesDict = {}

dirs = os.listdir('vul')
for d in dirs:
	path = "vul/" + d
	files = os.listdir(path)
	for f in files:
		if f.endswith('OLD.vul'):
			with open(os.path.join(path, f), "r") as fp:
				lines = ''.join(fp.readlines())
			body = p.getBody(lines)
			# body = lines[lines.find('{')+1:lines.rfind('}')]
			bodySplit = body.split('\n')
			finalList = []
			for b in bodySplit:
				if len(b) > 1:
					finalList.append(b)
			numLines = len(finalList)
			# if numLines == 2:
			# 	print path, f
			# 	print lines
			# 	print body
			# 	print body.split('\n')
			# 	sys.exit()
			try:
				linesDict[numLines] += 1
			except:
				linesDict[numLines] = 1

keyList = sorted(linesDict.keys())
for key in range(3467):
	if key in keyList:
		print str(key) + "\t" + str(linesDict[key])
	else:
		print str(key) + "\t" + str(0)
		# sys.exit()
		# numLines = len(lines.find('{')+1:)