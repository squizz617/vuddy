from antlr4 import *
from antlr4.tree.Trees import Trees
from ModuleLexer import ModuleLexer
from ModuleListener import ModuleListener
from ModuleParser import ModuleParser
import sys

class TreePrinterListener(ModuleListener):
    
    def __init__(self, parser):
        self.ruleNames = parser.ruleNames
        self.strbuilder = ""
    
    def enterEveryRule(self, ctx):
        ruleIndex = ctx.getRuleIndex()
        ruleName = ""
        
        if (ruleIndex >= 0 and ruleIndex < len(self.ruleNames)):
            ruleName = self.ruleNames[ruleIndex]
        else:
            ruleName = str(ruleIndex)
        
        (dwStart, dwStop) = ctx.getSourceInterval()
        dwLine = 0
        dwDepth = ctx.depth()
        self.strbuilder += (ruleName + '\t' + str(dwDepth) + '\t' + str(dwLine) + '\t' + str(dwStart) + '\t' + str(dwStop) + '\n');
        
    def visitTerminal(self, node):
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
