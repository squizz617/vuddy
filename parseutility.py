import os
import sys
import subprocess
import re

javaCallCommand = "java -jar CodeSensor.jar "

class function:
	parentFile = None 	# Absolute file which has the function
	name = None 		# Name of the function
	lines = None 		# Tuple (lineFrom, lineTo) that indicates the LoC of function
	funcId = None 		# n, indicating n-th function in the file
	parameterList = []	# list of parameter variables
	variableList = []	# list of local variables
	dataTypeList = []	# list of data types, including user-defined types
	funcCalleeList = []	# list of called functions' names

	def __init__(self, fileName):
		self.parentFile = fileName
		self.parameterList = []
		self.variableList = []
		self.dataTypeList = []
		self.funcCalleeList = []

	def removeListDup(self):
		self.parameterList = list(set(self.parameterList))
		self.variableList = list(set(self.variableList))
		self.dataTypeList = list(set(self.dataTypeList))
		self.funcCalleeList = list(set(self.funcCalleeList))

	def getOriginalFunction(self):
		fp = open(self.parentFile, 'r')
		srcFileRaw = fp.readlines()
		fp.close()
		return ''.join(srcFileRaw[self.lines[0]-1:self.lines[1]])


def loadSource(rootDirectory):
	maxFileSizeInBytes = 2097152
	walkList = os.walk(rootDirectory)
	srcFileList = []
	for path, dirs, files in walkList:
		for fileName in files:
			if fileName.endswith('.c') or fileName.endswith('.cpp') or fileName.endswith('.cc'):
				absPathWithFileName = path.replace('\\', '/') + '/' + fileName
				if os.path.getsize(absPathWithFileName) < maxFileSizeInBytes:
					srcFileList.append(absPathWithFileName)
	return srcFileList


def removeComment(string):
	c_regex = re.compile(r'(?P<comment>//.*?$|[{}]+)|(?P<multilinecomment>/\*.*?\*/)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^/\'"]*)', re.DOTALL | re.MULTILINE)
	return ''.join([c.group('noncomment') for c in c_regex.finditer(string) if c.group('noncomment')])


def getBody(originalFunction):
	return originalFunction[originalFunction.find('{')+1:originalFunction.rfind('}')]


def normalize(string):
	return ''.join(string.replace('\n', '').replace('\t','').replace('{', '').replace('}', '').split(' ')).lower()


def abstract(instance, level):
	# print "LEVEL", level
	originalFunction = instance.getOriginalFunction()
	originalFunction = removeComment(originalFunction)

	if int(level) >= 0:
		originalFunctionBody = getBody(originalFunction)
		abstractBody = originalFunctionBody

	if int(level) >= 1:	#PARAM
		parameterList = instance.parameterList
		for param in parameterList:
			paramPattern = re.compile("(^|\W)" + param + "(\W)")
			abstractBody = paramPattern.sub("\g<1>FPARAM\g<2>", originalFunctionBody)

	if int(level) >= 2:	#DTYPE
		dataTypeList = instance.dataTypeList
		for dtype in dataTypeList:
			dtypePattern = re.compile("(^|\W)" + dtype + "(\W)")
			abstractBody = dtypePattern.sub("\g<1>DTYPE\g<2>", abstractBody)

	if int(level) >= 3:	#LVAR
		variableList = instance.variableList
		for lvar in variableList:
			lvarPattern = re.compile("(^|\W)" + lvar + "(\W)")
			abstractBody = lvarPattern.sub("\g<1>LVAR\g<2>", abstractBody)

	if int(level) >= 4:	#FUNCCALL
		funcCalleeList = instance.funcCalleeList
		for fcall in funcCalleeList:
			fcallPattern = re.compile("(^|\W)" + fcall + "(\W)")
			abstractBody = fcallPattern.sub("\g<1>FUNCCALL\g<2>", abstractBody)

	return (originalFunctionBody, abstractBody)


def parseFile(srcFileName):
	fp = open(srcFileName, 'r')
	srcFileRaw = fp.readlines()
	fp.close()

	functionInstanceList = []
	paramDeclFlag = 0
	varDeclFlag = 0
	init = 0

	try:
		astString = subprocess.check_output(javaCallCommand + srcFileName, stderr=subprocess.STDOUT, shell=True)
	except subprocess.CalledProcessError as e:
		print "CodeSensor Error:", e
		astString = ""

	# print astString
	astLineList = astString.split('\n')
	for astLine in astLineList:
		astLineSplitted = astLine.split('\t')

		if "FUNCTION_DEF" == astLine[0:len("FUNCTION_DEF")]:
			init = 1
			functionInstance = function(srcFileName)
			functionInstanceList.append(functionInstance)
			functionInstance.funcId = len(functionInstanceList)
			(funcLineFrom, funcLineTo) = (int(astLineSplitted[1].split(':')[0]), int(astLineSplitted[2].split(':')[0]))
			functionInstance.lines = (funcLineFrom, funcLineTo)
		
		elif "FUNCTION_NAME" == astLine[0:len("FUNCTION_NAME")] and init:
			functionInstance.name = astLineSplitted[4].rstrip()

		elif "PARAMETER_DECL" == astLine[0:len("PARAMETER_DECL")] and init:
			paramDeclFlag = 1

		elif "VAR_DECL" == astLine[0:len("VAR_DECL")] and init:
			varDeclFlag = 1
		
		elif "NAME" == astLine[0:len("NAME")] and init:
			if paramDeclFlag:
				functionInstance.parameterList.append(astLineSplitted[4].rstrip())
				paramDeclFlag = 0
			elif varDeclFlag:
				functionInstance.variableList.append(astLineSplitted[4].rstrip())
				varDeclFlag = 0
		
		elif "TYPE_NAME" == astLine[0:len("TYPE_NAME")] and init:
			functionInstance.dataTypeList.append(astLineSplitted[4].rstrip())

		elif "CALLEE" == astLine[0:len("CALLEE")] and init:
			functionInstance.funcCalleeList.append(astLineSplitted[4].rstrip())

	return functionInstanceList


if __name__ == "__main__":
	targetDir = "C:\Users\Squizz-CCS\Documents\CCSLAB\RES_Zeroday_2016\HTTPD\httpd-2.4.20"
	targetDir = r"C:\Users\Squizz-CCS\Desktop\testcode"

	srcFileList = load(targetDir)

	for srcFile in srcFileList:
		print srcFile

		functionInstanceList = parseFile(srcFile)

		for f in functionInstanceList:
			f.removeListDup()
			print f.name, f.lines
			print "PARAMS\t", f.parameterList
			print "LVARS\t", f.variableList
			print "DTYPE\t", f.dataTypeList
			print "CALLS\t", f.funcCalleeList
			print ""
			abstract(f, 4)

		sys.exit()