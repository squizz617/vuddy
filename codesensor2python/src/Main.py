#!/bin/python

from antlr4 import *
from antlr4.tree.Trees import Trees

from FunctionLexer import FunctionLexer
from FunctionListener import FunctionListener
from FunctionParser import FunctionParser

from ModuleLexer import ModuleLexer
from ModuleListener import ModuleListener
from ModuleParser import ModuleParser
from cStringIO import StringIO
import sys

class FunctionListener(FunctionListener):

    def __init__(self, parser, line = 0):
        if line:
            line -= 1
        self.defaultLine = line
        self.ruleNames = parser.ruleNames
        self.strbuilder = ""

    def enterEveryRule(self, ctx):
        ruleIndex = ctx.getRuleIndex()
        ruleName = ""
        
        if (ruleIndex >= 0 and ruleIndex < len(self.ruleNames)):
            ruleName = self.ruleNames[ruleIndex]
        else:
            ruleName = str(ruleIndex)
        
        szStart = str((ctx.start.line + self.defaultLine)) + ":" + str(ctx.start.column)
        szStop = str((ctx.stop.line + self.defaultLine)) + ":" + str(ctx.stop.column)
        dwDepth = ctx.depth()
        self.strbuilder += (ruleName + '\t' + szStart + '\t' + szStop + '\t' + str(dwDepth) + '\n');
    
    def exitEveryRule(self, ctx):
        ruleIndex = ctx.getRuleIndex()
        ruleName = ""
        
        if (ruleIndex >= 0 and ruleIndex < len(self.ruleNames)):
            ruleName = self.ruleNames[ruleIndex]
        else:
            ruleName = str(ruleIndex)
        
        self.strbuilder += ("----- EXIT : " + ruleName + '\n')
        
    def visitTerminal(self, node):
        self.strbuilder = self.strbuilder[:-1]
        self.strbuilder += ("\t" + Trees.getNodeText(node) + '\n')



class TreePrinterListener(ModuleListener):
    
    def __init__(self, parser):
        self.ruleNames = parser.ruleNames
        self.strbuilder = ""
        
        self.compoundStmtFlag = False
    
    def print_compoundstmt(self, text, line):
        input = InputStream(text)
        lexer = FunctionLexer(input)
        stream = CommonTokenStream(lexer)
        parser = FunctionParser(stream)
        tree = parser.statements()
        
        listener = FunctionListener(parser, line)
        ParseTreeWalker().walk(listener, tree)
        
        return listener.strbuilder
        
    def enterEveryRule(self, ctx):
        ruleIndex = ctx.getRuleIndex()
        ruleName = ""
        
        if (ruleIndex >= 0 and ruleIndex < len(self.ruleNames)):
            ruleName = self.ruleNames[ruleIndex]
        else:
            ruleName = str(ruleIndex)
        
        #(dwStart, dwStop) = ctx.getSourceInterval()
        #dwLine = ctx.stop.line
        szStart = str(ctx.start.line) + ":" + str(ctx.start.column)
        szStop = str(ctx.stop.line) + ":" + str(ctx.stop.column)
        dwDepth = ctx.depth()
        #self.strbuilder += (ruleName + '\t' + str(dwDepth) + '\t' + str(dwLine) + '\t' + str(dwStart) + '\t' + str(dwStop) + '\n');
        self.strbuilder += (ruleName + '\t' + szStart + '\t' + szStop + '\t' + str(dwDepth) + '\n');
        
        
        if ruleName == "compound_statement":
            self.compoundStmtFlag = True
            #print "\tType(ctx): ", type(ctx)
            stream = ctx.start.getInputStream()
            #print inputstream
            #print type(ctx.start.stop)
            start_index = ctx.start.stop # start.start?
            stop_index = ctx.stop.stop
            print "compound_statement line: ", ctx.start.line
            self.strbuilder += self.print_compoundstmt(stream.getText(start_index, stop_index), ctx.start.line)
    
    def exitEveryRule(self, ctx):
        ruleIndex = ctx.getRuleIndex()
        ruleName = ""
        
        if (ruleIndex >= 0 and ruleIndex < len(self.ruleNames)):
            ruleName = self.ruleNames[ruleIndex]
        else:
            ruleName = str(ruleIndex)
        
        if ruleName == "compound_statement":
            self.compoundStmtFlag = False
        
        self.strbuilder += ("----- EXIT : " + ruleName + '\n')
        
    def visitTerminal(self, node):
        if not self.compoundStmtFlag:
            self.strbuilder = self.strbuilder[:-1]
            #self.strbuilder += ("\t" + Trees.getNodeText(node, self.ruleNames) + '\n')
            self.strbuilder += ("\t" + Trees.getNodeText(node) + '\n')

def main(argv):
    input = FileStream(argv[1])
    lexer = ModuleLexer(input)
    stream = CommonTokenStream(lexer)
    parser = ModuleParser(stream)
    tree = parser.code()
    
    listener = TreePrinterListener(parser)
    ParseTreeWalker().walk(listener, tree)
    
    print listener.strbuilder,

if __name__ == "__main__":
    main(sys.argv)
