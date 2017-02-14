"""
Parser utility.
Author: Seulbae Kim
Created: August 03, 2016
"""

import os
import sys
import subprocess
import re
import platform

def get_version():
	global osName
	global bits

	pf = platform.platform()
	if 'Windows' in pf:
		osName = 'w'
	elif 'Linux' in pf:
		osName = 'l'
	else:
		osName = 'osx'

	bits, _ = platform.architecture()
	if '64' in bits:
		bits = '64'
	else:
		bits = '86'

	if osName == 'osx':
		bits = ''

# sys.path.append(sys._MEIPASS)

def setEnvironment(caller):
	get_version()
	global javaCallCommand
	if caller == "GUI":
		# try:
		# 	base_path = sys._MEIPASS
		# except:
		# 	base_path = os.path.abspath(".")
		cwd = os.getcwd()
		if osName == 'w':
			# full_path = os.path.join(base_path, "FuncParser.exe")
			javaCallCommand = os.path.join(cwd, "FuncParser-opt.exe ")

		elif osName == 'l' or osName == "osx":
			# full_path = os.path.join(base_path, "FuncParser.jar")
			# javaCallCommand = "java -Xmx1024m -jar " + full_path + " "
			javaCallCommand = "java -Xmx1024m -jar \"" + os.path.join(cwd, "FuncParser-opt.jar") + "\" "

	else:
		if osName == 'w':
			javaCallCommand = "FuncParser-opt.exe "
		elif osName == 'l' or osName == "osx":
			javaCallCommand = "java -Xmx1024m -jar \"FuncParser-opt.jar\" "


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
	funcBody = None

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

	# def getOriginalFunction(self):
	# 	# returns the original function back from the instance.
	# 	fp = open(self.parentFile, 'r')
	# 	srcFileRaw = fp.readlines()
	# 	fp.close()
	# 	return ''.join(srcFileRaw[self.lines[0]-1:self.lines[1]])


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


# def getBody(originalFunction):
# 	# returns the function's body as a string.
# 	return originalFunction[originalFunction.find('{')+1:originalFunction.rfind('}')]


def normalize(string):
	# Code for normalizing the input string.
	# LF and TAB literals, curly braces, and spaces are removed,
	# and all characters are lowercased.
	return ''.join(string.replace('\n', '').replace('\t','').replace('{', '').replace('}', '').split(' ')).lower()


def abstract(instance, level):
	# Applies abstraction on the function instance,
	# and then returns a tuple consisting of the original body and abstracted body.
	originalFunctionBody = instance.funcBody
	originalFunctionBody = removeComment(originalFunctionBody)
	# print originalFunctionBody
	# print '===================================================='
	if int(level) >= 0:	# No abstraction.
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

delimiter = "\r\0?\r?\0\r"

def parseFile_shallow(srcFileName, caller):
	# this does not parse body.
	global javaCallCommand
	global delimiter

	setEnvironment(caller)
	javaCallCommand += "\"" + srcFileName + "\" 0"
	functionInstanceList = []
	try:
		astString = subprocess.check_output(javaCallCommand, stderr=subprocess.STDOUT, shell=True)
	except subprocess.CalledProcessError as e:
		print "Parser Error:", e
		astString = ""

	funcList = astString.split(delimiter)
	for func in funcList[1:]:
		functionInstance = function(srcFileName)
		elemsList = func.split('\n')[1:-1]
		# print elemsList
		if len(elemsList) > 9:
			functionInstance.parentNumLoc = int(elemsList[1])
			functionInstance.name = elemsList[2]
			functionInstance.lines = (int(elemsList[3].split('\t')[0]), int(elemsList[3].split('\t')[1]))
			functionInstance.funcId = int(elemsList[4])
			functionInstance.funcBody = ''.join(elemsList[9:])
			# print functionInstance.funcBody
			# print "-------------------"

			functionInstanceList.append(functionInstance)

	return functionInstanceList

def parseFile_deep(srcFileName, caller):
	global javaCallCommand
	global delimiter

	setEnvironment(caller)
	# this parses function definition plus body.
	javaCallCommand += "\"" + srcFileName + "\" 1"

	functionInstanceList = []

	try:
		astString = subprocess.check_output(javaCallCommand, stderr=subprocess.STDOUT, shell=True)
	except subprocess.CalledProcessError as e:
		print "Parser Error:", e
		astString = ""

	funcList = astString.split(delimiter)
	for func in funcList[1:]:
		functionInstance = function(srcFileName)

		elemsList = func.split('\n')[1:-1]
		# print elemsList
		if len(elemsList) > 9:
			functionInstance.parentNumLoc = int(elemsList[1])
			functionInstance.name = elemsList[2]
			functionInstance.lines = (int(elemsList[3].split('\t')[0]), int(elemsList[3].split('\t')[1]))
			functionInstance.funcId = int(elemsList[4])
			functionInstance.parameterList = elemsList[5].rstrip().split('\t')
			functionInstance.variableList = elemsList[6].rstrip().split('\t')
			functionInstance.dataTypeList = elemsList[7].rstrip().split('\t')
			functionInstance.funcCalleeList = elemsList[8].rstrip().split('\t')
			functionInstance.funcBody = ''.join(elemsList[9:])
			# print '\n'.join(elemsList[9:])
			functionInstanceList.append(functionInstance)

	return functionInstanceList
