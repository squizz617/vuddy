import parseutility
import sys

targetDir = "C:\Users\Squizz-CCS\Documents\CCSLAB\RES_Zeroday_2016\HTTPD\httpd-2.4.20"
targetDir = r"C:\Users\Squizz-CCS\Desktop\testcode"

srcFileList = parseutility.loadSource(targetDir)

for srcFile in srcFileList:
	print srcFile

	functionInstanceList = parseutility.parseFile(srcFile)

	# print functionsList
	for f in functionInstanceList:
		f.removeListDup()
		print f.name, f.lines
		print "PARAMS\t", f.parameterList
		print "LVARS\t", f.variableList
		print "DTYPE\t", f.dataTypeList
		print "CALLS\t", f.funcCalleeList
		print ""
		# print "[ORIGINAL]"
		# print f.getOriginalFunction()
		# print ""
		# print f.getOriginalFunction()[::-1]

		# print "================="
		(originalFunctionBody, abstractBody) = parseutility.abstract(f, 4)
		print parseutility.normalize(abstractBody)
		print "-----------------"

	sys.exit()