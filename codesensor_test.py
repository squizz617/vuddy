import os
import sys
import subprocess
import re

from loader import load

class function:
	parentFile = None
	name = None
	lines = None
	parameterList = []
	variableList = []
	dataTypeList = []
	funcCalleeList = []

	def __init__(self, fileName):
		# print "INIT"
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


def normalize(string):
	return ''.join(string.replace('\n', '').replace('\t','').replace('{', '').replace('}', '').split(' ')).lower()


def removeComment(string):
	c_regex = re.compile(r'(?P<comment>//.*?$|[{}]+)|(?P<multilinecomment>/\*.*?\*/)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^/\'"]*)', re.DOTALL | re.MULTILINE)
	return ''.join([c.group('noncomment') for c in c_regex.finditer(string) if c.group('noncomment')])


def getBody(originalFunction):
	return originalFunction[originalFunction.find('{')+1:originalFunction.rfind('}')]

def abstraction(instance, level):
	print "LEVEL", level
	originalFunction = instance.getOriginalFunction()

	if int(level) >= 0:
		print "[L0]\t", originalFunction
		functionBody = getBody(originalFunction)
		print "[L0N]\t", normalize(removeComment(functionBody)), "\n"

	if int(level) >= 1:	#PARAM
		parameterList = instance.parameterList
		for param in parameterList:
			paramPattern = re.compile("(^|\W)" + param + "(\W)")
			originalFunction = paramPattern.sub("\g<1>FPARAM\g<2>", originalFunction)
		print "[L1]\t", originalFunction

		functionBody = getBody(originalFunction)
		print "[L1N]\t", normalize(removeComment(functionBody)), "\n"

	if int(level) >= 2:	#DTYPE
		dataTypeList = instance.dataTypeList
		for dtype in dataTypeList:
			dtypePattern = re.compile("(^|\W)" + dtype + "(\W)")
			originalFunction = dtypePattern.sub("\g<1>DTYPE\g<2>", originalFunction)
		print "[L2]\t", originalFunction
		functionBody = getBody(originalFunction)
		print "[L2N]\t", normalize(removeComment(functionBody)), "\n"

	if int(level) >= 3:	#LVAR
		variableList = instance.variableList
		for lvar in variableList:
			lvarPattern = re.compile("(^|\W)" + lvar + "(\W)")
			originalFunction = lvarPattern.sub("\g<1>LVAR\g<2>", originalFunction)
		print "[L3]\t", originalFunction
		functionBody = getBody(originalFunction)
		print "[L3N]\t", normalize(removeComment(functionBody)), "\n"

	if int(level) >= 4:	#FUNCCALL
		funcCalleeList = instance.funcCalleeList
		for fcall in funcCalleeList:
			fcallPattern = re.compile("(^|\W)" + fcall + "(\W)")
			originalFunction = fcallPattern.sub("\g<1>FUNCCALL\g<2>", originalFunction)
		print "[L4]\t", originalFunction
		functionBody = getBody(originalFunction)
		print "[L4N]\t", normalize(removeComment(functionBody)), "\n"


targetDir = "C:\Users\Squizz-CCS\Documents\CCSLAB\RES_Zeroday_2016\HTTPD\httpd-2.4.20"
targetDir = r"C:\Users\Squizz-CCS\Desktop\testcode"
command = "java -jar CodeSensor.jar "

srcFileList = load(targetDir)


for srcFile in srcFileList:
	print srcFile
	functionsList = []
	paramDeclFlag = 0
	varDeclFlag = 0
	init = 0

	fp = open(srcFile, 'r')
	srcFileRaw = fp.readlines()
	fp.close()

	try:
		astString = subprocess.check_output(command + srcFile, stderr=subprocess.STDOUT, shell=False)
	except subprocess.CalledProcessError as e:
		print "CodeSensor Error:", e
		astString = ""

	print astString
	astLineList = astString.split('\n')
	for astLine in astLineList:
		astLineSplitted = astLine.split('\t')

		if "FUNCTION_DEF" == astLine[0:len("FUNCTION_DEF")]:
			init = 1
			func = function(srcFile)
			functionsList.append(func)
			(funcLineFrom, funcLineTo) = (int(astLineSplitted[1].split(':')[0]), int(astLineSplitted[2].split(':')[0]))
			func.lines = (funcLineFrom, funcLineTo)
		
		elif "FUNCTION_NAME" == astLine[0:len("FUNCTION_NAME")] and init:
			func.name = astLineSplitted[4].rstrip()

		# elif "PARAMETER_LIST" == astLine[0:len("PARAMETER_LIST")] and init:
		# 	paramsList.append(astLineSplitted[4].rstrip())
		
		elif "PARAMETER_DECL" == astLine[0:len("PARAMETER_DECL")] and init:
			paramDeclFlag = 1

		elif "VAR_DECL" == astLine[0:len("VAR_DECL")] and init:
			varDeclFlag = 1
		
		elif "NAME" == astLine[0:len("NAME")] and init:
			if paramDeclFlag:
				func.parameterList.append(astLineSplitted[4].rstrip())
				paramDeclFlag = 0
			elif varDeclFlag:
				func.variableList.append(astLineSplitted[4].rstrip())
				varDeclFlag = 0
		
		elif "TYPE_NAME" == astLine[0:len("TYPE_NAME")] and init:
			func.dataTypeList.append(astLineSplitted[4].rstrip())

		elif "CALLEE" == astLine[0:len("CALLEE")] and init:
			func.funcCalleeList.append(astLineSplitted[4].rstrip())

	# print functionsList
	for f in functionsList:
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
		abstraction(f, 4)
		# print "-----------------"

	sys.exit()