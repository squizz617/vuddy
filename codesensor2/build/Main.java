
import org.antlr.v4.runtime.ANTLRFileStream;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.ParseTreeListener;
import org.antlr.v4.runtime.Parser;
//import org.antlr.v4.runtime.tree.TerminalNode;
import org.antlr.v4.runtime.tree.*;
import org.antlr.v4.runtime.ParserRuleContext;
import org.antlr.v4.runtime.RuleContext;
import org.antlr.v4.runtime.misc.Utils;

import org.antlr.v4.runtime.Token;

import java.io.*;
import java.util.List;
import java.util.Arrays;
import java.util.ArrayList;

public class Main {
	public static void main(String[] args) throws IOException
	{
		try {
			String inputFilename = parseCommandLine(args);
			ANTLRFileStream  antlrFileStream = new ANTLRFileStream(inputFilename);
			ModuleLexer lexer = new ModuleLexer(antlrFileStream);
			CommonTokenStream tokens = new CommonTokenStream(lexer);
			ModuleParser parser = new ModuleParser(tokens);
			ParseTree tree = parser.code();
			/*
			//System.out.println(tree.getText());
			System.out.println(tree);
			if (tree.getChild(0) instanceof ParseTree)
				System.out.println("parse tree");
			if (tree.getChild(0) instanceof RuleContext)
				System.out.println("rule context");
			if (tree.getChild(0) instanceof ParserRuleContext)
				System.out.println("parser rule context");
			if (tree.getChild(0) instanceof Token)
				System.out.println("token");
			
			System.out.println(tree.getPayload());
			if (tree.getPayload() instanceof ParseTree)
				System.out.println("ParseTree");
			if (tree.getPayload() instanceof RuleContext)
				System.out.println("RuleContext");
			if (tree.getPayload() instanceof ParserRuleContext)
				System.out.println("ParserRuleContext");
			if (tree.getPayload() instanceof Token)
				System.out.println("Token");
			
			System.out.println("");
			//System.out.println(tree.toStringTree(parser));
			System.out.println("");*/
			
			TreePrinterListener listener = new TreePrinterListener(parser);
			ParseTreeWalker.DEFAULT.walk(listener, tree);
			
			System.out.println(listener.toString());
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	private static String parseCommandLine(String[] args) throws Exception
	{
		if(args.length != 1) {
			throw new Exception("filename required.");
		}
		
		return args[0];
	}
}

class TreePrinterListener implements ParseTreeListener {
	private final List<String> ruleNames;
	private final StringBuilder strbuilder = new StringBuilder();
	
	public TreePrinterListener(Parser parser) {
		this.ruleNames = Arrays.asList(parser.getRuleNames());
	}
	
	public TreePrinterListener(List<String> ruleNames) {
		this.ruleNames = ruleNames;
	}
	
	@Override
	public void visitTerminal(TerminalNode node) {
		strbuilder.setLength(strbuilder.length() - 1);
		strbuilder.append("\t" + Utils.escapeWhitespace(Trees.getNodeText(node, ruleNames), false) + '\n');
	}
	
	@Override
	public void visitErrorNode(ErrorNode node) {
		strbuilder.setLength(strbuilder.length() - 1);
		strbuilder.append("\t" + Utils.escapeWhitespace(Trees.getNodeText(node, ruleNames), false) + '\n');
	}
	
	@Override
	public void enterEveryRule(ParserRuleContext ctx) {
		int ruleIndex = ctx.getRuleIndex();
		String ruleName;
		
		if (ruleIndex >= 0 && ruleIndex < ruleNames.size())
			ruleName = ruleNames.get(ruleIndex);
		else
			ruleName = Integer.toString(ruleIndex);
		
		int dwLine = 0, dwStart = 0, dwStop = 0, dwDepth = 0;
		String strText = "";
		Token positionToken = ctx.getStart();
		if (positionToken != null)
		{
			dwLine = positionToken.getLine();
			dwStart = positionToken.getStartIndex();
			dwStop = positionToken.getStopIndex();
			dwDepth = ctx.depth();
			strText = ctx.getText();
		}
		
		//System.out.println(ruleName + '\t' + dwDepth + '\t' + dwLine + '\t' + dwStart +'\t' + dwStop + '\t' + strText);
		strbuilder.append(ruleName + '\t' + dwDepth + '\t' + dwLine + '\t' + dwStart +'\t' + dwStop + '\n');
	}
	
	@Override
	public void exitEveryRule(ParserRuleContext ctx) {}
	
	@Override
	public String toString() {
		return strbuilder.toString();
	}
}

class AST {

    /**
     * The payload will either be the name of the parser rule, or the token
     * of a leaf in the tree.
     */
    private final Object payload;

    /**
     * All child nodes of this AST.
     */
    private final List<AST> children;

    public AST(ParseTree tree) {
        this(null, tree);
    }

    private AST(AST ast, ParseTree tree) {
        this(ast, tree, new ArrayList<AST>());
    }

    private AST(AST parent, ParseTree tree, List<AST> children) {

        this.payload = getPayload(tree);
        this.children = children;

        if (parent == null) {
            // We're at the root of the AST, traverse down the parse tree to fill
            // this AST with nodes.
            walk(tree, this);
        }
        else {
            parent.children.add(this);
        }
    }

    public Object getPayload() {
        return payload;
    }

    public List<AST> getChildren() {
        return new ArrayList<>(children);
    }

    // Determines the payload of this AST: a string in case it's an inner node (which
    // is the name of the parser rule), or a Token in case it is a leaf node.
    private Object getPayload(ParseTree tree) {
        if (tree.getChildCount() == 0) {
            // A leaf node: return the tree's payload, which is a Token.
            return tree.getPayload();
        }
        else {
            // The name for parser rule `foo` will be `FooContext`. Strip `Context` and
            // lower case the first character.
            String ruleName = tree.getClass().getSimpleName().replace("Context", "");
            return Character.toLowerCase(ruleName.charAt(0)) + ruleName.substring(1);
        }
    }

    // Fills this AST based on the parse tree.
    private static void walk(ParseTree tree, AST ast) {

        if (tree.getChildCount() == 0) {
            // We've reached a leaf. We must create a new instance of an AST because
            // the constructor will make sure this new instance is added to its parent's
            // child nodes.
            new AST(ast, tree);
        }
        else if (tree.getChildCount() == 1) {
            // We've reached an inner node with a single child: we don't include this in
            // our AST.
            walk(tree.getChild(0), ast);
        }
        else if (tree.getChildCount() > 1) {

            for (int i = 0; i < tree.getChildCount(); i++) {

                AST temp = new AST(ast, tree.getChild(i));

                if (!(temp.payload instanceof Token)) {
                    // Only traverse down if the payload is not a Token.
                    walk(tree.getChild(i), temp);
                }
            }
        }
    }

    @Override
    public String toString() {

        StringBuilder builder = new StringBuilder();

        AST ast = this;
        List<AST> firstStack = new ArrayList<>();
        firstStack.add(ast);

        List<List<AST>> childListStack = new ArrayList<>();
        childListStack.add(firstStack);

        while (!childListStack.isEmpty()) {

            List<AST> childStack = childListStack.get(childListStack.size() - 1);

            if (childStack.isEmpty()) {
                childListStack.remove(childListStack.size() - 1);
            }
            else {
                ast = childStack.remove(0);
                String caption;

                if (ast.payload instanceof Token) {
                    Token token = (Token) ast.payload;
                    caption = String.format("TOKEN[type: %s, text: %s]",
                            token.getType(), token.getText().replace("\n", "\\n"));
                }
                else {
                    caption = String.valueOf(ast.payload);
                }

                String indent = "";

                for (int i = 0; i < childListStack.size() - 1; i++) {
                    indent += (childListStack.get(i).size() > 0) ? "|  " : "   ";
                }

                builder.append(indent)
                        .append(childStack.isEmpty() ? "'- " : "|- ")
                        .append(caption)
                        .append("\n");

                if (ast.children.size() > 0) {
                    List<AST> children = new ArrayList<>();
                    for (int i = 0; i < ast.children.size(); i++) {
                        children.add(ast.children.get(i));
                    }
                    childListStack.add(children);
                }
            }
        }

        return builder.toString();
    }
}
