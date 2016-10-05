#!/bin/python

from antlr4 import *
from antlr4.tree.Trees import Trees
from antlr4.error.ErrorStrategy import DefaultErrorStrategy
from codesensor2python.build.ModuleLexer import ModuleLexer
from codesensor2python.build.ModuleListener import ModuleListener
from codesensor2python.build.ModuleParser import ModuleParser
from codesensor2python.build.FunctionLexer import FunctionLexer
from codesensor2python.build.FunctionListener import FunctionListener
from codesensor2python.build.FunctionParser import FunctionParser
from parseutility import function, abstract

from cStringIO import StringIO
import sys

class BodyParser(FunctionListener):
	IS_FIRST = 1
	FUNCTION_DEF = 0
	FUNCTION_NAME = 1
	PARAMETER_NAME = 2
	DECLARATOR = 3
	TYPE_NAME = 4
	FUNCTION_CALL = 5
	COMPOUND_STMT = 6
	
	table = ["function_def", "function_name", "parameter_name", "declarator", "type_name", "identifier", "compound_statement"]
	IDX = [0, 0, 0, 0, 0, 0, 0]
	
	
	def __init__(self):
		self.functionInstance = None
		
		# Function body's base line
		self.defaultLine = 0
		'''
		# Function's name
		self.funcNameFlag = 0
		self.funcNameStr = StringIO()
		
		# Function parameter's name
		self.paramNameFlag = 0
		self.paramNameStr = StringIO()
		'''
		# Local variable's name
		self.declaratorFlag = 0
		self.declaratorStr = StringIO()
		
		# type (return type, parameter type, local variable type)
		self.typeNameFlag = 0
		self.typeNameStr = StringIO()
		'''
		# function definition
		self.funcDefFlag = 0
		'''
		self.funcCallFlag = 0
		self.funcCallStr = StringIO()
		'''
		# function body (compound_statement)
		self.compoundStmtFlag = 0

		self.srcFileName = ""
		self.numLines = 0 # ??
		'''
		# set SLL option
		self.enableSLL = 0
	
	def _init(self, parser):
		self.__init__()
		
		if BodyParser.IS_FIRST:
			for i, ruleName in enumerate(parser.ruleNames):
				for j, tableName in enumerate(BodyParser.table):
					if ruleName == tableName:
						BodyParser.IDX[j] = i
		BodyParser.IS_FIRST = 0
	
	
	def ParseString(self, string, funcinstance, line = 0, bSLL = 1):
		input = InputStream(string)
		lexer = FunctionLexer(input)
		stream = CommonTokenStream(lexer)
		parser = FunctionParser(stream)
		parser.removeErrorListeners() # remove error listener
		
		if bSLL:
			#print "start parsing in BodyParser class with SLL mode"
			parser._interp.predictionMode = PredictionMode.SLL
			parser._errHandler = BailErrorStrategy() # BailErrorStrategy() reports error
		try:
			tree = parser.statements()
		except error.Errors.ParseCancellationException:
			#print "Exception found in BodyParser class. set LL mode"
			parser.reset()
			parser._interp.predictionMode = PredictionMode.LL
			parser._errHandler = DefaultErrorStrategy()
			tree = parser.statements()
		self._init(parser) # reset before traverse a parse tree
		self.enableSLL = bSLL
		
		self.functionInstance = funcinstance
		if line: # if line is zero, self.defaultLine is also zero
			self.defaultLine = (line - 1)
		
		ParseTreeWalker().walk(self, tree)
		
	
	def enterEveryRule(self, ctx):
		ruleIndex = ctx.getRuleIndex()
		'''
		if ruleIndex == TreeParser.IDX[TreeParser.FUNCTION_DEF]:
			self.funcDefFlag = 1
			self.functionInstance = function(self.srcFileName)
			#self.functionInstanceList.append(self.functionInstance)
			self.functionInstance.parentNumLoc = self.numLines #????
			self.functionInstance.funcId = len(self.functionInstanceList)
			self.functionInstance.lines = (ctx.start.line, ctx.stop.line)
		
		elif ruleIndex == TreeParser.IDX[TreeParser.FUNCTION_NAME]:
			self.funcNameFlag = 1
		
		elif ruleIndex == TreeParser.IDX[TreeParser.PARAMETER_NAME]:
			self.paramNameFlag = 1
		'''
		if ruleIndex == BodyParser.IDX[BodyParser.DECLARATOR]:
			self.declaratorFlag = 1
		
		elif ruleIndex == BodyParser.IDX[BodyParser.TYPE_NAME]:
			self.typeNameFlag = 1

		elif ruleIndex == BodyParser.IDX[BodyParser.FUNCTION_CALL]:
			self.funcCallFlag = 1
		'''
		elif ruleIndex == TreeParser.IDX[TreeParser.COMPOUND_STMT]:
			self.compoundStmtFlag = 1
		'''
	
	
	def exitEveryRule(self, ctx):
		ruleIndex = ctx.getRuleIndex()
		'''
		if ruleIndex == TreeParser.IDX[TreeParser.FUNCTION_DEF] and self.funcDefFlag:
			#print "INIT"
			self.funcDefFlag = 0
			self.functionInstanceList.append(self.functionInstance)
		elif ruleIndex == TreeParser.IDX[TreeParser.FUNCTION_NAME] and self.funcNameFlag:
			#print "NAME"
			self.functionInstance.name = self.funcNameStr.getvalue().rstrip()
			self.funcNameFlag = 0
			self.funcNameStr = StringIO()
		elif ruleIndex == TreeParser.IDX[TreeParser.PARAMETER_NAME] and self.paramNameFlag:
			#print "PARAM"
			self.functionInstance.parameterList.append(self.paramNameStr.getvalue().rstrip())
			self.paramNameFlag = 0
			self.paramNameStr = StringIO()
		'''
		if ruleIndex == BodyParser.IDX[BodyParser.DECLARATOR] and self.declaratorFlag: # useless if-statement (because, enter declarator -> exit identifier)
			#print "LVAR"
			self.functionInstance.variableList.append(self.declaratorStr.getvalue().rstrip())
			self.declaratorFlag = 0
			self.declaratorStr = StringIO()
		elif ruleIndex == BodyParser.IDX[BodyParser.TYPE_NAME] and self.typeNameFlag:
			#print "DTYPE"
			self.functionInstance.dataTypeList.append(self.typeNameStr.getvalue().rstrip())
			self.typeNameFlag = 0
			self.typeNameStr = StringIO()
		elif ruleIndex == BodyParser.IDX[BodyParser.FUNCTION_CALL] and self.funcCallFlag:
			#print "CALL"
			if self.funcCallFlag == 2:
				self.functionInstance.funcCalleeList.append(self.funcCallStr.getvalue().rstrip())
			self.funcCallFlag = 0
			self.funcCallStr = StringIO()
			
			if self.declaratorFlag: # [enter declarator -> exit identifier]: avoid "a [ 1 ]" in local variable name
				self.functionInstance.variableList.append(self.declaratorStr.getvalue().rstrip())
				self.declaratorFlag = 0
				self.declaratorStr = StringIO()
		'''
		elif ruleIndex == TreeParser.IDX[TreeParser.COMPOUND_STMT] and self.compoundStmtFlag:
			self.compoundStmtFlag = 0
		'''
	
	def visitTerminal(self, node):
		'''
		if self.compoundStmtFlag:
			return
		
		elif self.funcNameFlag:
			self.funcNameStr.write(Trees.getNodeText(node))
			self.funcNameStr.write(' ')
		
		elif self.paramNameFlag:
			self.paramNameStr.write(Trees.getNodeText(node))
			self.paramNameStr.write(' ')
		'''
		if self.declaratorFlag:
			tmpText = Trees.getNodeText(node)
			
			if tmpText != "*": # remove pointer(*) in name of local variables
				self.declaratorStr.write(tmpText)
				self.declaratorStr.write(' ')
		
		elif self.typeNameFlag:
			self.typeNameStr.write(Trees.getNodeText(node))
			self.typeNameStr.write(' ')

		elif self.funcCallFlag:
			try:
				parentNodes = node.getParent()
				p1 = parentNodes
				p2 = p1.parentCtx
				p3 = p2.parentCtx
				p4 = p3.parentCtx	# walk up to its fourth parent
			except AttributeError:
				pass
			else:
				if str(type(p4)).endswith("FuncCallContext'>"):
					self.funcCallStr.write(Trees.getNodeText(node))
					self.funcCallStr.write(' ')
					self.funcCallFlag = 2


class TreeParser(ModuleListener):
	IS_FIRST = 1
	FUNCTION_DEF = 0
	FUNCTION_NAME = 1
	PARAMETER_NAME = 2
	DECLARATOR = 3
	TYPE_NAME = 4
	FUNCTION_CALL = 5
	COMPOUND_STMT = 6
	
	table = ["function_def", "function_name", "parameter_name", "declarator", "type_name", "identifier", "compound_statement"]
	IDX = [0, 0, 0, 0, 0, 0, 0]
	
	
	def __init__(self):
		self.functionInstanceList = []
		self.functionInstance = None
		
		# Function's name
		self.funcNameFlag = 0
		self.funcNameStr = StringIO()
		
		# Function parameter's name
		self.paramNameFlag = 0
		self.paramNameStr = StringIO()
		
		# Local variable's name
		self.declaratorFlag = 0
		self.declaratorStr = StringIO()
		
		# type (return type, parameter type, local variable type)
		self.typeNameFlag = 0
		self.typeNameStr = StringIO()
		
		# function definition
		self.funcDefFlag = 0
		
		self.funcCallFlag = 0
		self.funcCallStr = StringIO()
		
		# function body (compound_statement)
		self.compoundStmtFlag = 0
		
		self.srcFileName = ""
		self.numLines = 0 # ??
		
		# set SLL option
		self.enableSLL = 0
	
	def _init(self, parser):
		self.__init__()
		
		if TreeParser.IS_FIRST:
			for i, ruleName in enumerate(parser.ruleNames):
				for j, tableName in enumerate(TreeParser.table):
					if ruleName == tableName:
						TreeParser.IDX[j] = i
		TreeParser.IS_FIRST = 0
	
	
	def ParseFile(self, srcFileName, bSLL = 1):
		input = FileStream(srcFileName)
		lexer = ModuleLexer(input)
		stream = CommonTokenStream(lexer)
		parser = ModuleParser(stream)
		parser.removeErrorListeners()
		
		if bSLL:
			#print "start parsing in TreeParser class with SLL mode"
			parser._interp.predictionMode = PredictionMode.SLL
			#parser._errHandler = DefaultErrorStrategy()
			parser._errHandler = BailErrorStrategy() # BailErrorStrategy() reports error
		try:
			tree = parser.code()
		except error.Errors.ParseCancellationException:
			#print "Exception found in TreeParser class. set LL mode"
			parser.reset()
			parser._interp.predictionMode = PredictionMode.LL
			parser._errHandler = DefaultErrorStrategy()
			tree = parser.code()
		self._init(parser) # reset before traverse a parse tree
		self.enableSLL = bSLL
		
		fp = open(srcFileName, 'r')
		srcFileRaw = fp.readlines()
		fp.close()
		self.numLines = len(srcFileRaw) #???
		self.srcFileName = srcFileName
		
		ParseTreeWalker().walk(self, tree)
		
		return self.functionInstanceList
	
	
	def enterEveryRule(self, ctx):
		ruleIndex = ctx.getRuleIndex()

		if ruleIndex == TreeParser.IDX[TreeParser.FUNCTION_DEF]:
			self.funcDefFlag = 1
			self.functionInstance = function(self.srcFileName)
			#self.functionInstanceList.append(self.functionInstance)
			self.functionInstance.parentNumLoc = self.numLines #????
			self.functionInstance.funcId = len(self.functionInstanceList)
			self.functionInstance.lines = (ctx.start.line, ctx.stop.line)
		
		elif not self.funcDefFlag:
			return
		
		elif ruleIndex == TreeParser.IDX[TreeParser.FUNCTION_NAME]:
			self.funcNameFlag = 1
		
		elif ruleIndex == TreeParser.IDX[TreeParser.PARAMETER_NAME]:
			self.paramNameFlag = 1
		
		elif ruleIndex == TreeParser.IDX[TreeParser.DECLARATOR]:
			self.declaratorFlag = 1
		
		elif ruleIndex == TreeParser.IDX[TreeParser.TYPE_NAME]:
			self.typeNameFlag = 1

		elif ruleIndex == TreeParser.IDX[TreeParser.FUNCTION_CALL]:
			self.funcCallFlag = 1
		
		elif ruleIndex == TreeParser.IDX[TreeParser.COMPOUND_STMT]:
			self.compoundStmtFlag = 1
	
	
	def exitEveryRule(self, ctx):
		ruleIndex = ctx.getRuleIndex()

		if ruleIndex == TreeParser.IDX[TreeParser.FUNCTION_DEF] and self.funcDefFlag:
			#print "INIT"
			self.funcDefFlag = 0
			self.functionInstanceList.append(self.functionInstance)
		elif ruleIndex == TreeParser.IDX[TreeParser.FUNCTION_NAME] and self.funcNameFlag:
			#print "NAME"
			self.functionInstance.name = self.funcNameStr.getvalue().rstrip()
			self.funcNameFlag = 0
			self.funcNameStr = StringIO()
		elif ruleIndex == TreeParser.IDX[TreeParser.PARAMETER_NAME] and self.paramNameFlag:
			#print "PARAM"
			self.functionInstance.parameterList.append(self.paramNameStr.getvalue().rstrip())
			self.paramNameFlag = 0
			self.paramNameStr = StringIO()
		elif ruleIndex == TreeParser.IDX[TreeParser.DECLARATOR] and self.declaratorFlag:
			#print "LVAR"
			self.functionInstance.variableList.append(self.declaratorStr.getvalue().rstrip())
			self.declaratorFlag = 0
			self.declaratorStr = StringIO()
		elif ruleIndex == TreeParser.IDX[TreeParser.TYPE_NAME] and self.typeNameFlag:
			#print "DTYPE"
			self.functionInstance.dataTypeList.append(self.typeNameStr.getvalue().rstrip())
			self.typeNameFlag = 0
			self.typeNameStr = StringIO()
		elif ruleIndex == TreeParser.IDX[TreeParser.FUNCTION_CALL] and self.funcCallFlag:
			#print "CALL"
			if self.funcCallFlag == 2:
				self.functionInstance.funcCalleeList.append(self.funcCallStr.getvalue().rstrip())
			self.funcCallFlag = 0
			self.funcCallStr = StringIO()
		elif ruleIndex == TreeParser.IDX[TreeParser.COMPOUND_STMT] and self.compoundStmtFlag:
			self.compoundStmtFlag = 0
			line = ctx.start.line
			start_index = ctx.start.stop # start.start?
			stop_index = ctx.stop.stop
			stream = ctx.start.getInputStream()
			string = stream.getText(start_index, stop_index)
			BodyParser().ParseString(string, self.functionInstance, line, self.enableSLL)
	
	def visitTerminal(self, node):
		if self.compoundStmtFlag or not self.funcDefFlag:
			return
		elif self.funcNameFlag:
			self.funcNameStr.write(Trees.getNodeText(node))
			self.funcNameStr.write(' ')
		
		elif self.paramNameFlag:
			self.paramNameStr.write(Trees.getNodeText(node))
			self.paramNameStr.write(' ')
		
		elif self.declaratorFlag:
			tmpText = Trees.getNodeText(node)

			if tmpText != "*": # remove pointer(*) in name of local variables
				self.declaratorStr.write(tmpText)
				self.declaratorStr.write(' ')
		
		elif self.typeNameFlag:
			self.typeNameStr.write(Trees.getNodeText(node))
			self.typeNameStr.write(' ')

		elif self.funcCallFlag:
			try:
				parentNodes = node.getParent()
				p1 = parentNodes
				p2 = p1.parentCtx
				p3 = p2.parentCtx
				p4 = p3.parentCtx	# walk up to its fourth parent
			except AttributeError:
				pass
			else:
				if str(type(p4)).endswith("FuncCallContext'>"):
					self.funcCallStr.write(Trees.getNodeText(node))
					self.funcCallStr.write(' ')
					self.funcCallFlag = 2


def main(argv):
	import time
	t1 = time.time()
	functionInstanceList = TreeParser().ParseFile(argv[1])
	print argv[1]
	t2 = time.time()
	# sys.exit()
	for f in functionInstanceList:
		f.removeListDup()
		print f.name, f.lines
		print "PARAMS\t", f.parameterList, "\n"
		print "LVARS\t", f.variableList, "\n"
		print "DTYPE\t", f.dataTypeList, "\n"
		print "CALLS\t", f.funcCalleeList, "\n"
		print ""

		abstract(f, 4)

	t3 = time.time()

	print "parse %.4f" %(t2 - t1)
	print "print %.4f" %(t3 - t2)
	sys.exit()

if __name__ == "__main__":
	main(sys.argv)
