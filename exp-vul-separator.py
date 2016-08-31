import os
import sys
import parseutility

repoList = os.listdir('vul')
originDir = os.getcwd()
targetDir = os.path.join(os.getcwd(), "vul-per-length")
print originDir, targetDir
for repo in repoList:
	print "Processing", repo
	vulList = os.listdir(os.path.join("vul", repo))
	for vul in vulList:
		if not vul.endswith("_OLD.vul"):
			continue
		filePathandName = os.path.join("vul", repo, vul)
		# with open(filePathandName, "r") as fp:
			# vulContent = fp.readlines()
		funcInstanceList = parseutility.parseFile(filePathandName)
		f = funcInstanceList[0]
		f.removeListDup()
		abstractBody = parseutility.abstract(f, 0)[1]
		lineCnt = 0
		for line in abstractBody.split('\n'):
			normLine = parseutility.normalize(line)
			if len(normLine) > 1:
				lineCnt += 1
		# print lineCnt

		try:
			os.mkdir(os.path.join(targetDir, str(lineCnt)))
		except:
			pass
		newFilePathandName = os.path.join(targetDir, str(lineCnt), vul)
		# print newFilePathandName
		os.system("cp " + filePathandName + " " + newFilePathandName)
		# print vulContent
		# sys.exit()
	# print os.path.join()