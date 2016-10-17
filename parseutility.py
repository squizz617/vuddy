"""
Parser utility.
Author: Seulbae Kim
Created: August 03, 2016
"""

import os
import sys
import subprocess
import re

# javaCallCommand = "java -jar CodeSensor.jar "

class function:
	parentFile = None 	# Absolute file which has the function
	parentNumLoc = None # Number of LoC of the parent file
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
		# for best performance, must execute this method
		# for every instance before applying the abstraction.
		self.parameterList = list(set(self.parameterList))
		self.variableList = list(set(self.variableList))
		self.dataTypeList = list(set(self.dataTypeList))
		self.funcCalleeList = list(set(self.funcCalleeList))

	def getOriginalFunction(self):
		# returns the original function back from the instance.
		fp = open(self.parentFile, 'r')
		srcFileRaw = fp.readlines()
		fp.close()
		return ''.join(srcFileRaw[self.lines[0]-1:self.lines[1]])


def loadSource(rootDirectory):
	# returns the list of .src files under the specified root directory.
	maxFileSizeInBytes = None
	maxFileSizeInBytes = 2097152	# remove this line if you don't want to restrict
									# the maximum file size that you process.
	walkList = os.walk(rootDirectory)
	srcFileList = []
	for path, dirs, files in walkList:
		for fileName in files:
			if fileName.endswith('.c') or fileName.endswith('.cpp'):# or fileName.endswith('.cc'):
				absPathWithFileName = path.replace('\\', '/') + '/' + fileName
				if maxFileSizeInBytes is not None:
					if os.path.getsize(absPathWithFileName) < maxFileSizeInBytes:
						srcFileList.append(absPathWithFileName)
				else:
					srcFileList.append(absPathWithFileName)
	return srcFileList

def loadVul(rootDirectory):
	# returns the list of .vul files under the specified root directory.
	maxFileSizeInBytes = None
	# maxFileSizeInBytes = 2097152	# remove this line if you don't want to restrict
									# the maximum file size that you process.
	walkList = os.walk(rootDirectory)
	srcFileList = []
	for path, dirs, files in walkList:
		for fileName in files:
			if fileName.endswith('OLD.vul'):
				absPathWithFileName = path.replace('\\', '/') + '/' + fileName
				if maxFileSizeInBytes is not None:
					if os.path.getsize(absPathWithFileName) < maxFileSizeInBytes:
						srcFileList.append(absPathWithFileName)
				else:
					srcFileList.append(absPathWithFileName)
	return srcFileList


def removeComment(string):
	# Code for removing C/C++ style comments. (Imported from ReDeBug.)
	c_regex = re.compile(r'(?P<comment>//.*?$|[{}]+)|(?P<multilinecomment>/\*.*?\*/)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^/\'"]*)', re.DOTALL | re.MULTILINE)
	return ''.join([c.group('noncomment') for c in c_regex.finditer(string) if c.group('noncomment')])


def getBody(originalFunction):
	# returns the function's body as a string.
	return originalFunction[originalFunction.find('{')+1:originalFunction.rfind('}')]


def normalize(string):
	# Code for normalizing the input string.
	# LF and TAB literals, curly braces, and spaces are removed,
	# and all characters are lowercased.
	return ''.join(string.replace('\n', '').replace('\t','').replace('{', '').replace('}', '').split(' ')).lower()


def abstract(instance, level):
	# Applies abstraction on the function instance,
	# and then returns a tuple consisting of the original body and abstracted body.
	originalFunction = instance.getOriginalFunction()
	originalFunction = removeComment(originalFunction)

	if int(level) >= 0:	# No abstraction.
		originalFunctionBody = getBody(originalFunction)
		abstractBody = originalFunctionBody

	if int(level) >= 1:	# PARAM
		parameterList = instance.parameterList
		for param in parameterList:
			if len(param) == 0:
				continue
			try:
				paramPattern = re.compile("(^|\W)" + param + "(\W)")
				abstractBody = paramPattern.sub("\g<1>FPARAM\g<2>", abstractBody)
			except:
				pass

	if int(level) >= 2:	# DTYPE
		dataTypeList = instance.dataTypeList
		for dtype in dataTypeList:
			if len(dtype) == 0:
				continue
			try:
				dtypePattern = re.compile("(^|\W)" + dtype + "(\W)")
				abstractBody = dtypePattern.sub("\g<1>DTYPE\g<2>", abstractBody)
			except:
				pass

	if int(level) >= 3:	# LVAR
		variableList = instance.variableList
		for lvar in variableList:
			if len(lvar) == 0:
				continue
			try:
				lvarPattern = re.compile("(^|\W)" + lvar + "(\W)")
				abstractBody = lvarPattern.sub("\g<1>LVAR\g<2>", abstractBody)
			except:
				pass

	if int(level) >= 4:	# FUNCCALL
		funcCalleeList = instance.funcCalleeList
		for fcall in funcCalleeList:
			if len(fcall) == 0:
				continue
			try:
				fcallPattern = re.compile("(^|\W)" + fcall + "(\W)")
				abstractBody = fcallPattern.sub("\g<1>FUNCCALL\g<2>", abstractBody)
			except:
				pass

	return (originalFunctionBody, abstractBody)


# def abstractWindow(instance, level, lineList):
# 	# Do not use this function.

# 	if int(level) >= 0:
# 		originalFunctionBody = '\n'.join(lineList)
# 		abstractBody = originalFunctionBody

# 	if int(level) >= 1:	#PARAM
# 		parameterList = instance.parameterList
# 		for param in parameterList:
# 			paramPattern = re.compile("(^|\W)" + param + "(\W)")
# 			abstractBody = paramPattern.sub("\g<1>FPARAM\g<2>", originalFunctionBody)

# 	if int(level) >= 2:	#DTYPE
# 		dataTypeList = instance.dataTypeList
# 		for dtype in dataTypeList:
# 			dtypePattern = re.compile("(^|\W)" + dtype + "(\W)")
# 			abstractBody = dtypePattern.sub("\g<1>DTYPE\g<2>", abstractBody)

# 	if int(level) >= 3:	#LVAR
# 		variableList = instance.variableList
# 		for lvar in variableList:
# 			lvarPattern = re.compile("(^|\W)" + lvar + "(\W)")
# 			abstractBody = lvarPattern.sub("\g<1>LVAR\g<2>", abstractBody)

# 	if int(level) >= 4:	#FUNCCALL
# 		funcCalleeList = instance.funcCalleeList
# 		for fcall in funcCalleeList:
# 			fcallPattern = re.compile("(^|\W)" + fcall + "(\W)")
# 			abstractBody = fcallPattern.sub("\g<1>FUNCCALL\g<2>", abstractBody)

# 	return (originalFunctionBody, abstractBody)


# def parseFile(srcFileName):
# 	# Parses the functions of the specified file using CodeSensor.jar
# 	# and then returns the list of function instances.
# 	fp = open(srcFileName, 'r')
# 	srcFileRaw = fp.readlines()
# 	fp.close()
# 	numLines = len(srcFileRaw)
# 	functionInstanceList = []
# 	paramDeclFlag = 0
# 	varDeclFlag = 0
# 	init = 0

# 	try:
# 		astString = subprocess.check_output(javaCallCommand + srcFileName, stderr=subprocess.STDOUT, shell=True)
# 	except subprocess.CalledProcessError as e:
# 		print "CodeSensor Error:", e
# 		astString = ""

# 	astLineList = astString.split('\n')
# 	for astLine in astLineList:
# 		astLineSplitted = astLine.split('\t')

# 		if "FUNCTION_DEF" == astLine[0:len("FUNCTION_DEF")]:
# 			init = 1
# 			functionInstance = function(srcFileName)
# 			functionInstanceList.append(functionInstance)
# 			functionInstance.parentNumLoc = numLines
# 			functionInstance.funcId = len(functionInstanceList)
# 			(funcLineFrom, funcLineTo) = (int(astLineSplitted[1].split(':')[0]), int(astLineSplitted[2].split(':')[0]))
# 			functionInstance.lines = (funcLineFrom, funcLineTo)
		
# 		elif "FUNCTION_NAME" == astLine[0:len("FUNCTION_NAME")] and init:
# 			functionInstance.name = astLineSplitted[4].rstrip()

# 		elif "PARAMETER_DECL" == astLine[0:len("PARAMETER_DECL")] and init:
# 			paramDeclFlag = 1

# 		elif "VAR_DECL" == astLine[0:len("VAR_DECL")] and init:
# 			varDeclFlag = 1
		
# 		elif "NAME" == astLine[0:len("NAME")] and init:
# 			if paramDeclFlag:
# 				functionInstance.parameterList.append(astLineSplitted[4].rstrip())
# 				paramDeclFlag = 0
# 			elif varDeclFlag:
# 				functionInstance.variableList.append(astLineSplitted[4].rstrip())
# 				varDeclFlag = 0
		
# 		elif "TYPE_NAME" == astLine[0:len("TYPE_NAME")] and init:
# 			functionInstance.dataTypeList.append(astLineSplitted[4].rstrip())

# 		elif "CALLEE" == astLine[0:len("CALLEE")] and init:
# 			functionInstance.funcCalleeList.append(astLineSplitted[4].rstrip())

# 	return functionInstanceList

def parseFile_shallow(srcFileName):
	# this does not parse body.
	javaCallCommand = "java -Xmx1024m -jar FuncParser.jar " + srcFileName + " 0"
	functionInstanceList = []
	try:
		astString = subprocess.check_output(javaCallCommand, stderr=subprocess.STDOUT, shell=True)
	except subprocess.CalledProcessError as e:
		print "Parser Error:", e
		astString = ""

	funcList = astString.split('\r')
	for func in funcList[1:]:
		functionInstance = function(srcFileName)
		functionInstanceList.append(functionInstance)

		elemsList = func.split('\n')[1:-1]
		functionInstance.parentNumLoc = int(elemsList[1])
		functionInstance.name = elemsList[2]
		functionInstance.lines = (int(elemsList[3].split('\t')[0]), int(elemsList[3].split('\t')[1]))
		functionInstance.funcId = int(elemsList[4])

	return functionInstanceList

def parseFile_deep(srcFileName):
	# this parses function definition plus body.
	javaCallCommand = "java -Xmx1024m -jar FuncParser.jar " + srcFileName + " 1"

	# fp = open(srcFileName, 'r')
	# srcFileRaw = fp.readlines()
	# fp.close()
	# numLines = len(srcFileRaw)
	functionInstanceList = []

	try:
		astString = subprocess.check_output(javaCallCommand, stderr=subprocess.STDOUT, shell=True)
	except subprocess.CalledProcessError as e:
		print "Parser Error:", e
		astString = ""

	funcList = astString.split('\r')
	for func in funcList[1:]:
		functionInstance = function(srcFileName)
		functionInstanceList.append(functionInstance)

		elemsList = func.split('\n')[1:-1]
		functionInstance.parentNumLoc = int(elemsList[1])
		functionInstance.name = elemsList[2]
		functionInstance.lines = (int(elemsList[3].split('\t')[0]), int(elemsList[3].split('\t')[1]))
		functionInstance.funcId = int(elemsList[4])
		functionInstance.parameterList = elemsList[5].rstrip().split('\t')
		functionInstance.variableList = elemsList[6].rstrip().split('\t')
		functionInstance.dataTypeList = elemsList[7].rstrip().split('\t')
		functionInstance.funcCalleeList = elemsList[8].rstrip().split('\t')

	return functionInstanceList



if __name__ == "__main__":
	# Just for testing.
	# targetDir = "C:\Users\Squizz-CCS\Documents\CCSLAB\RES_Zeroday_2016\HTTPD\httpd-2.4.20"
	# targetDir = r"C:\Users\Squizz-CCS\Desktop\testcode"

	# srcFileList = loadSource(targetDir)

	# for srcFile in srcFileList:
		# print srcFile

	# srcFile = "/home/squizz/Downloads/SM-G930S-G930SKSU1APB2/Kernel/arch/x86/kernel/ldt.c"
	srcFile = "../kernel44/arch/um/kernel/syscall.c"
	srcFile = "./module.c"
	functionInstanceList = parseFile2(srcFile)

	for f in functionInstanceList:
		f.removeListDup()
		print f.name, f.lines
		print "PARAMS\t", f.parameterList
		print "LVARS\t", f.variableList
		print "DTYPE\t", f.dataTypeList
		print "CALLS\t", f.funcCalleeList
		print ""
		na = normalize(abstract(f, 4)[1])
		import hashlib
		print hashlib.md5(na).hexdigest()

	sys.exit()