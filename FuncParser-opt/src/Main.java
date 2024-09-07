
import org.antlr.v4.runtime.ANTLRFileStream;
import org.antlr.v4.runtime.ANTLRInputStream;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.ParseTreeListener;
import org.antlr.v4.runtime.Parser;
//import org.antlr.v4.runtime.tree.TerminalNode;
import org.antlr.v4.runtime.tree.*;
import org.antlr.v4.runtime.ParserRuleContext;
import org.antlr.v4.runtime.RuleContext;
import org.antlr.v4.runtime.misc.Utils;
import org.antlr.v4.runtime.misc.ParseCancellationException;

import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.misc.Interval;

import org.antlr.v4.runtime.DefaultErrorStrategy;
import org.antlr.v4.runtime.BailErrorStrategy;
import org.antlr.v4.runtime.atn.PredictionMode;

import org.antlr.v4.runtime.Token;

import java.io.*;
import java.util.List;
import java.util.Arrays;
import java.util.ArrayList;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.Callable;


public class Main {
	public static void main(String[] args) throws IOException {
		List<function> ret;
		long t1, t2, t3;
		try {
			String inputFilename = parseCommandLine(args);
			String bParseBody = "1"; // "1": with body parser, "0": without body parser
			if (args.length > 1)
				bParseBody = args[args.length - 1];
			if (!bParseBody.equals("0") && !bParseBody.equals("1"))
				throw new Exception("argument bParseBody(last argument) required.");
			
			//System.out.println("processors: " + Runtime.getRuntime().availableProcessors());
			t1 = System.currentTimeMillis();
			if (bParseBody.equals("1")) {
				TreeParser tp = new TreeParser();
				ret = tp.ParseFile(inputFilename);
			}
			else {
				TreeParser1 tp = new TreeParser1();
				ret = tp.ParseFile(inputFilename);
			}
			t2 = System.currentTimeMillis();
		} catch (Exception e) {
			e.printStackTrace();
			return;
		}
		
		print_functions_all(ret); // print_functions() or print_functions_all()
		t3 = System.currentTimeMillis();
		
		//System.out.println("parse " + (t2 - t1) / 1000.0);
		//System.out.println("print " + (t3 - t2) / 1000.0);
	}
	
	// Print all elements in function class seperated with CR, LF, TAB.
	// Please refer function.toString() method.
	private static void print_functions_all(List<function> func_list) {
		for (function f : func_list)
			System.out.print(f);
	}
	
	// Print name, line, parameter, variable, datatype and funccallee in function class.
	private static void print_functions(List<function> func_list) {
		System.out.println("func_list.size(): " + func_list.size());
		int i = 0;
		for (function f : func_list) {
			System.out.println("" + (i++) + ": " + f.name + 
					"(" + f.lineStart + ", " + f.lineStop + ")");
			
			System.out.print("  PARAM\t[");
			for (String element : f.parameterList)
				System.out.print(element + ", ");
			System.out.println("]");
			
			System.out.print("  LVARS\t[");
			for (String element : f.variableList)
				System.out.print(element + ", ");
			System.out.println("]");
			
			System.out.print("  DTYPE\t[");
			for (String element : f.dataTypeList)
				System.out.print(element + ", ");
			System.out.println("]");
			
			System.out.print("  CALLS\t[");
			for (String element : f.funcCalleeList)
				System.out.print(element + ", ");
			System.out.println("]\n");
		}
	}
	
	private static String parseCommandLine(String[] args) throws Exception {
		if(args.length < 1) {
			throw new Exception("filename required.");
		}
		
		return args[0];
	}
}

class function {
	public String parentFile;
	public int parentNumLoc = 0;
	public String name;
	public int lineStart = 0;
	public int lineStop = 0;
	public int funcId = 0;
	public String funcBody;
	
	public List<String> parameterList;
	public List<String> variableList;
	public List<String> dataTypeList;
	public List<String> funcCalleeList;
	
	function(String fileName) {
		this.parentFile = fileName;
		this.parameterList = new ArrayList<String>();
		this.variableList = new ArrayList<String>();
		this.dataTypeList = new ArrayList<String>();
		this.funcCalleeList = new ArrayList<String>();
	}
	
	public String toString() {
		StringBuilder ret = new StringBuilder();
		
		ret.append("\r\0?\r?\0\r"); // function string start
		ret.append('\n');
		
		ret.append(parentFile);
		ret.append('\n');
		
		ret.append(String.valueOf(parentNumLoc));
		ret.append('\n');
		
		ret.append(name);
		ret.append('\n');
		
		ret.append(String.valueOf(lineStart));
		ret.append('\t');
		ret.append(String.valueOf(lineStop));
		ret.append('\n');
		
		ret.append(String.valueOf(funcId));
		ret.append('\n');
		
		for (String s : this.parameterList) {
			ret.append(s);
			ret.append('\t');
		}
		ret.append('\n');
		for (String s : this.variableList) {
			ret.append(s);
			ret.append('\t');
		}
		ret.append('\n');
		for (String s : this.dataTypeList) {
			ret.append(s);
			ret.append('\t');
		}
		ret.append('\n');
		for (String s : this.funcCalleeList) {
			ret.append(s);
			ret.append('\t');
		}
		ret.append('\n');
		
		ret.append(this.funcBody);
		ret.append('\n');
		
		return ret.toString();
	}	
}

class JobInstance implements Callable<function> {
	public function functionInstance;
	public String string;
	public int line;
	public int enableSLL;
	
	public JobInstance(String s, function f, int l, int e) {
		this.functionInstance = f;
		this.string = s;
		this.line = l;
		this.enableSLL = e;
	}
	
	public function call() throws Exception {
		//System.err.println("call() called: " + Thread.currentThread().getName());
		BodyParser p = new BodyParser();
		p.ParseString(this.string, this.functionInstance, this.line, this.enableSLL);
		return this.functionInstance;
	}
}

class BodyParser implements ParseTreeListener {
	private static int IS_FIRST = 1;
	
	public final static int FUNCTION_DEF = 0;
	public final static int FUNCTION_NAME = 1;
	public final static int PARAMETER_NAME = 2;
	public final static int DECLARATOR = 3;
	public final static int TYPE_NAME = 4;
	public final static int FUNCTION_CALL = 5;
	public final static int COMPOUND_STMT = 6;
	
	private final static String[] table = {"function_def", "function_name", "parameter_name", 
				"declarator", "type_name", "identifier", "compound_statement"};
	private static int[] IDX = {0, 0, 0, 0, 0, 0, 0};
	
	private static List<String> ruleNames;
	
	private function functionInstance = null;
	
	// Function body's base line
	private int defaultLine = 0;
	
	// Local variable's name
	private int declaratorFlag = 0;
	private StringBuilder declaratorStr = new StringBuilder();
	
	// type (return type, parameter type, local variable type)
	private int typeNameFlag = 0;
	private StringBuilder typeNameStr = new StringBuilder();
	
	private int funcCallFlag = 0;
	private StringBuilder funcCallStr = new StringBuilder();
	
	// set SLL option
	private int enableSLL = 0;

	public BodyParser() {
		this.functionInstance = null;
		
		this.defaultLine = 0;

		this.declaratorFlag = 0;
		this.declaratorStr = new StringBuilder();
		
		// type (return type, parameter type, local variable type)
		this.typeNameFlag = 0;
		this.typeNameStr = new StringBuilder();
		
		this.funcCallFlag = 0;
		this.funcCallStr = new StringBuilder();
		
		// set SLL option
		this.enableSLL = 0;
	}
	
	private void _init(FunctionParser parser) {
		//this();
		this.functionInstance = null;
		
		this.defaultLine = 0;

		this.declaratorFlag = 0;
		this.declaratorStr = new StringBuilder();
		
		this.typeNameFlag = 0;
		this.typeNameStr = new StringBuilder();
		
		this.funcCallFlag = 0;
		this.funcCallStr = new StringBuilder();
		
		this.enableSLL = 0;
		
		if (BodyParser.IS_FIRST != 0) {
			this.ruleNames = Arrays.asList(parser.getRuleNames());
			
			for (int i = 0; i < parser.ruleNames.length; i++) {
				for (int j = 0; j < BodyParser.table.length; j++) {
					if (parser.ruleNames[i].equals(BodyParser.table[j]))
						BodyParser.IDX[j] = i;
				}
			}
			BodyParser.IS_FIRST = 0;
		}
	}
		
	public void ParseString(String string, function functionInstance) {
		this.ParseString(string, functionInstance, 0);
	}
	public void ParseString(String string, function functionInstance, int line) {
		this.ParseString(string, functionInstance, line, 1);
	}
	public void ParseString(String string, function funcinstance, int line, int bSLL) {
		try {
			ANTLRInputStream input = new ANTLRInputStream(string);
			FunctionLexer lexer = new FunctionLexer(input);
			CommonTokenStream tokens = new CommonTokenStream(lexer);
			FunctionParser parser = new FunctionParser(tokens);
			parser.removeErrorListeners(); // remove error listener
			
			if (bSLL != 0) {
				//print "start parsing in BodyParser class with SLL mode"
				parser.getInterpreter().setPredictionMode(PredictionMode.SLL);
				parser.setErrorHandler(new BailErrorStrategy());
			}
			
			ParseTree tree;
			try {
				tree = parser.statements();
			}
			catch (ParseCancellationException e) {
				//print "Exception found in BodyParser class. set LL mode"
				parser.reset();
				parser.getInterpreter().setPredictionMode(PredictionMode.LL);
				parser.setErrorHandler(new DefaultErrorStrategy());
				tree = parser.statements();
			}
			this._init(parser); // reset before traverse a parse tree
			this.enableSLL = bSLL;
			this.functionInstance = funcinstance;
			
			if (line != 0) // if line is zero, self.defaultLine is also zero
				this.defaultLine = (line - 1);
			
			//ParseTreeWalker ptw = new ParseTreeWalker();
			//ptw.walk(this, tree);
			ParseTreeWalker.DEFAULT.walk(this, tree);
		}
		catch (Exception e) {
			e.printStackTrace();
		}
		return;
	}
	
	@Override
	public void enterEveryRule(ParserRuleContext ctx) {
		int ruleIndex = ctx.getRuleIndex();
		
		if (ruleIndex == BodyParser.IDX[BodyParser.DECLARATOR])
			this.declaratorFlag = 1;
		else if (ruleIndex == BodyParser.IDX[BodyParser.TYPE_NAME])
			this.typeNameFlag = 1;
		else if (ruleIndex == BodyParser.IDX[BodyParser.FUNCTION_CALL])
			this.funcCallFlag = 1;
	}
	
	
	@Override
	public void exitEveryRule(ParserRuleContext ctx) {
		int ruleIndex = ctx.getRuleIndex();
		
		if (ruleIndex == BodyParser.IDX[BodyParser.DECLARATOR] && this.declaratorFlag != 0) {// useless if-statement (because, enter declarator -> exit identifier)
			//print "LVAR"
			this.functionInstance.variableList.add(this.declaratorStr.toString().trim());
			this.declaratorFlag = 0;
			this.declaratorStr.setLength(0);
		}
		else if (ruleIndex == BodyParser.IDX[BodyParser.TYPE_NAME] && this.typeNameFlag != 0) {
			//print "DTYPE"
			this.functionInstance.dataTypeList.add(this.typeNameStr.toString().trim());
			this.typeNameFlag = 0;
			this.typeNameStr.setLength(0);
		}
		else if (ruleIndex == BodyParser.IDX[BodyParser.FUNCTION_CALL] && this.funcCallFlag != 0) {
			//print "CALL"
			if (this.funcCallFlag == 2)
				this.functionInstance.funcCalleeList.add(this.funcCallStr.toString().trim());
			this.funcCallFlag = 0;
			this.funcCallStr.setLength(0);
			
			if (this.declaratorFlag != 0) {// [enter declarator -> exit identifier]: avoid "a [ 1 ]" in local variable name
				this.functionInstance.variableList.add(this.declaratorStr.toString().trim());
				this.declaratorFlag = 0;
				this.declaratorStr.setLength(0);
			}
		}
	}
		
	@Override
	public void visitTerminal(TerminalNode node) {
		if (this.declaratorFlag != 0) {
			String tmpText = Trees.getNodeText(node, this.ruleNames);
			
			if (!tmpText.equals("*")) {
				this.declaratorStr.append(tmpText);
				this.declaratorStr.append(' ');
			}
		}
		else if (this.typeNameFlag != 0) {
			this.typeNameStr.append(Trees.getNodeText(node, this.ruleNames));
			this.typeNameStr.append(' ');
		}
		else if (this.funcCallFlag != 0) {
			try {
				ParseTree p1 = node.getParent().getParent().getParent().getParent();
				
				//System.out.println("-----funcCallFlag: " + p1.getClass());
				if (p1 instanceof FunctionParser.FuncCallContext) {
					//System.out.println("found");
					this.funcCallStr.append(Trees.getNodeText(node ,this.ruleNames));
					this.funcCallStr.append(' ');
					this.funcCallFlag = 2;
				}
			}
			catch (Exception e) { // useless?
				//System.out.println("-----funcCallFlag: Exception found");
			}
		}
	}
	
	@Override
	public void visitErrorNode(ErrorNode node) { }
}

class TreeParser implements ParseTreeListener {
	private static int IS_FIRST = 1;
	
	public final static int FUNCTION_DEF = 0;
	public final static int FUNCTION_NAME = 1;
	public final static int PARAMETER_NAME = 2;
	public final static int DECLARATOR = 3;
	public final static int TYPE_NAME = 4;
	public final static int FUNCTION_CALL = 5;
	public final static int COMPOUND_STMT = 6;
	
	private final static String[] table = {"function_def", "function_name", "parameter_name", 
				"declarator", "type_name", "identifier", "compound_statement"};
	private static int[] IDX = {0, 0, 0, 0, 0, 0, 0};
	
	private static List<String> ruleNames;
	
	private ExecutorService executorService;
	private List<Future<function>> future_list = new ArrayList<Future<function>>(); // for multithread
	//private List<JobInstance> job_list = new ArrayList<JobInstance>(); // for singlethread
	private function functionInstance = null;
	
	// Function's name
	private int funcNameFlag = 0;
	private StringBuilder funcNameStr = new StringBuilder();
	
	// Function parameter's name
	private int paramNameFlag = 0;
	private StringBuilder paramNameStr = new StringBuilder(); //final?
	
	// type (return type, parameter type, local variable type)
	private int typeNameFlag = 0;
	private StringBuilder typeNameStr = new StringBuilder();
	
	// function definition
	private int funcDefFlag = 0;
	
	// function body (compund_statement)
	private int compoundStmtFlag = 0;
	
	private String srcFileName;
	private int numLines = 0;
	
	// set SLL option
	private int enableSLL = 0;
	
	
	public TreeParser() {
		this.functionInstance = null;
		
		this.funcNameFlag = 0;
		this.funcNameStr = new StringBuilder();
		
		this.paramNameFlag = 0;
		this.paramNameStr = new StringBuilder();
		
		this.typeNameFlag = 0;
		this.typeNameStr = new StringBuilder();
		
		this.funcDefFlag = 0;
		
		this.compoundStmtFlag = 0;
		
		this.enableSLL = 0;
	}
	
	private void _init(ModuleParser parser) {
		//this();
		this.executorService = Executors.newFixedThreadPool(
			Runtime.getRuntime().availableProcessors()
		);
		
		this.functionInstance = null;
		
		this.funcNameFlag = 0;
		this.funcNameStr = new StringBuilder();
		
		this.paramNameFlag = 0;
		this.paramNameStr = new StringBuilder();
		
		this.typeNameFlag = 0;
		this.typeNameStr = new StringBuilder();
		
		this.funcDefFlag = 0;
		
		this.compoundStmtFlag = 0;
		
		this.enableSLL = 0;
		
		
		if (TreeParser.IS_FIRST != 0) {
			this.ruleNames = Arrays.asList(parser.getRuleNames());
			
			for (int i = 0; i < parser.ruleNames.length; i++) {
				for (int j = 0; j < TreeParser.table.length; j++) {
					if (parser.ruleNames[i].equals(TreeParser.table[j]))
						TreeParser.IDX[j] = i;
				}
			}
		}
		TreeParser.IS_FIRST = 0;
	}
	
	public List<function> ParseFile(String srcFileName) {
		return this.ParseFile(srcFileName, 1);
	}
	public List<function> ParseFile(String srcFileName, int bSLL) {
		List<function> ret = new ArrayList<function>();
		try {
			ANTLRFileStream  antlrFileStream = new ANTLRFileStream(srcFileName);
			ModuleLexer lexer = new ModuleLexer(antlrFileStream);
			CommonTokenStream tokens = new CommonTokenStream(lexer);
			ModuleParser parser = new ModuleParser(tokens);
			parser.removeErrorListeners(); // remove error listener
			
			if (bSLL != 0) {
				parser.getInterpreter().setPredictionMode(PredictionMode.SLL);
				parser.setErrorHandler(new BailErrorStrategy());
			}
			
			//long t1 = System.currentTimeMillis();
			ParseTree tree;
			try {
				tree = parser.code();
			}
			catch (ParseCancellationException e) {
				parser.reset();
				parser.getInterpreter().setPredictionMode(PredictionMode.LL);
				parser.setErrorHandler(new DefaultErrorStrategy());
				tree = parser.code();
			}
			//long t2 = System.currentTimeMillis();
			//System.err.println("time: " + (t2 - t1) / 1000.0);
			this._init(parser); // reset before traverse a parse tree
			this.enableSLL = bSLL;
			
			LineNumberReader lnr = new LineNumberReader(new FileReader(new File(srcFileName)));
			while (lnr.skip(Long.MAX_VALUE) > 0);
			this.numLines = lnr.getLineNumber() + 1;
			lnr.close();
			
			this.srcFileName = new String(srcFileName);
			
			ParseTreeWalker.DEFAULT.walk(this, tree);
			
			//System.err.println("before get()");
			//long t3 = System.currentTimeMillis();
			for (Future<function> future : this.future_list) {
				ret.add(future.get());
			}
			//long t4 = System.currentTimeMillis();
			//System.err.println("time: " + (t4 - t3) / 1000.0);
			//System.err.println("after get()");
			/*
			for (int i = 0; i < job_list.size(); i++) { // singlethread
				JobInstance j = job_list.get(i);
				BodyParser p = new BodyParser();
				p.ParseString(j.string, j.functionInstance, j.line, j.enableSLL);
				ret.add(j.functionInstance);
			}
			*/

		} catch (Exception e) {
			e.printStackTrace();
			this.executorService.shutdownNow();
			return null;
		}
		this.executorService.shutdown();
		return ret;
	}
	
	@Override
	public void enterEveryRule(ParserRuleContext ctx) {
		int ruleIndex = ctx.getRuleIndex();
		
		if (ruleIndex == TreeParser.IDX[TreeParser.FUNCTION_DEF]) {
			this.funcDefFlag = 1;
			this.functionInstance = new function(this.srcFileName);
			this.functionInstance.parentNumLoc = this.numLines;
			this.functionInstance.funcId = this.future_list.size() + 1;
			this.functionInstance.lineStart = ctx.getStart().getLine();
			this.functionInstance.lineStop = ctx.getStop().getLine();
		}
		else if (this.funcDefFlag == 0)
			return;
		else if (ruleIndex == TreeParser.IDX[TreeParser.FUNCTION_NAME])
			this.funcNameFlag = 1;
		else if (ruleIndex == TreeParser.IDX[TreeParser.PARAMETER_NAME])
			this.paramNameFlag = 1;
		else if (ruleIndex == TreeParser.IDX[TreeParser.TYPE_NAME])
			this.typeNameFlag = 1;
		else if (ruleIndex == TreeParser.IDX[TreeParser.COMPOUND_STMT])
			this.compoundStmtFlag = 1;
	}
	
	@Override
	public void exitEveryRule(ParserRuleContext ctx) {
		int ruleIndex = ctx.getRuleIndex();
		
		if (ruleIndex == TreeParser.IDX[TreeParser.FUNCTION_DEF] && this.funcDefFlag != 0)
			this.funcDefFlag = 0;
		else if (ruleIndex == TreeParser.IDX[TreeParser.FUNCTION_NAME] && this.funcNameFlag != 0) {
			this.functionInstance.name = this.funcNameStr.toString().trim();
			this.funcNameFlag = 0;
			this.funcNameStr.setLength(0);
		}
		else if (ruleIndex == TreeParser.IDX[TreeParser.PARAMETER_NAME] && this.paramNameFlag != 0) {
			this.functionInstance.parameterList.add(this.paramNameStr.toString().trim());
			this.paramNameFlag = 0;
			this.paramNameStr.setLength(0);
		}
		else if (ruleIndex == TreeParser.IDX[TreeParser.TYPE_NAME] && this.typeNameFlag != 0) {
			this.functionInstance.dataTypeList.add(this.typeNameStr.toString().trim());
			this.typeNameFlag = 0;
			this.typeNameStr.setLength(0);
		}
		else if (ruleIndex == TreeParser.IDX[TreeParser.COMPOUND_STMT] && this.compoundStmtFlag != 0) {
			this.compoundStmtFlag = 0;
			
			CharStream inputStream = ctx.start.getInputStream();
			int start_index = ctx.start.getStopIndex();
			int stop_index = ctx.stop.getStopIndex();
			String string = inputStream.getText(new Interval(start_index + 1, stop_index - 1));
			int line = ctx.start.getLine();
			
			// add function's body
			this.functionInstance.funcBody = string;
			
			//this.job_list.add(new JobInstance(string, this.functionInstance, line, this.enableSLL)); // for singlethread
			this.future_list.add(
				this.executorService.submit(new JobInstance(string, this.functionInstance, line, this.enableSLL))
			); // for multithread
		}
	}
	
	@Override
	public void visitTerminal(TerminalNode node) {
		if (this.compoundStmtFlag != 0 || this.funcDefFlag == 0)
			return;
		else if (this.funcNameFlag != 0) {
			this.funcNameStr.append(Trees.getNodeText(node, this.ruleNames));
			this.funcNameStr.append(' ');
		}
		else if (this.paramNameFlag != 0) {
			this.paramNameStr.append(Trees.getNodeText(node, this.ruleNames));
			this.paramNameStr.append(' ');
		}
		else if (this.typeNameFlag != 0) {
			this.typeNameStr.append(Trees.getNodeText(node, this.ruleNames));
			this.typeNameStr.append(' ');
		}
	}
	
	@Override
	public void visitErrorNode(ErrorNode node) { }
}

class TreeParser1 implements ParseTreeListener {
	private static int IS_FIRST = 1;
	
	public final static int FUNCTION_DEF = 0;
	public final static int FUNCTION_NAME = 1;
	public final static int PARAMETER_NAME = 2;
	public final static int DECLARATOR = 3;
	public final static int TYPE_NAME = 4;
	public final static int FUNCTION_CALL = 5;
	public final static int COMPOUND_STMT = 6;
	
	private final static String[] table = {"function_def", "function_name", "parameter_name", 
				"declarator", "type_name", "identifier", "compound_statement"};
	private static int[] IDX = {0, 0, 0, 0, 0, 0, 0};
	
	private static List<String> ruleNames;
	
	//private ExecutorService executorService;
	//private List<Future<function>> future_list = new ArrayList<Future<function>>(); // for multithread
	//private List<JobInstance> job_list = new ArrayList<JobInstance>(); // for singlethread
	
	private List<function> ret;
	
	private function functionInstance = null;
	
	// Function's name
	private int funcNameFlag = 0;
	private StringBuilder funcNameStr = new StringBuilder();
	
	// Function parameter's name
	private int paramNameFlag = 0;
	private StringBuilder paramNameStr = new StringBuilder(); //final?
	
	// type (return type, parameter type, local variable type)
	private int typeNameFlag = 0;
	private StringBuilder typeNameStr = new StringBuilder();
	
	// function definition
	private int funcDefFlag = 0;
	
	// function body (compund_statement)
	private int compoundStmtFlag = 0;
	
	private String srcFileName;
	private int numLines = 0;
	
	// set SLL option
	private int enableSLL = 0;
	
	
	public TreeParser1() {
		this.ret = new ArrayList<function>();
		
		this.functionInstance = null;
		
		this.funcNameFlag = 0;
		this.funcNameStr = new StringBuilder();
		
		this.paramNameFlag = 0;
		this.paramNameStr = new StringBuilder();
		
		this.typeNameFlag = 0;
		this.typeNameStr = new StringBuilder();
		
		this.funcDefFlag = 0;
		
		this.compoundStmtFlag = 0;
		
		this.enableSLL = 0;
	}
	
	private void _init(ModuleParser parser) {
		//this();
		//this.executorService = Executors.newFixedThreadPool(
		//	Runtime.getRuntime().availableProcessors()
		//);
		this.ret = new ArrayList<function>();
		
		this.functionInstance = null;
		
		this.funcNameFlag = 0;
		this.funcNameStr = new StringBuilder();
		
		this.paramNameFlag = 0;
		this.paramNameStr = new StringBuilder();
		
		this.typeNameFlag = 0;
		this.typeNameStr = new StringBuilder();
		
		this.funcDefFlag = 0;
		
		this.compoundStmtFlag = 0;
		
		this.enableSLL = 0;
		
		
		if (TreeParser1.IS_FIRST != 0) {
			this.ruleNames = Arrays.asList(parser.getRuleNames());
			
			for (int i = 0; i < parser.ruleNames.length; i++) {
				for (int j = 0; j < TreeParser1.table.length; j++) {
					if (parser.ruleNames[i].equals(TreeParser1.table[j]))
						TreeParser1.IDX[j] = i;
				}
			}
		}
		TreeParser1.IS_FIRST = 0;
	}
	
	public List<function> ParseFile(String srcFileName) {
		return this.ParseFile(srcFileName, 1);
	}
	public List<function> ParseFile(String srcFileName, int bSLL) {
		try {
			ANTLRFileStream  antlrFileStream = new ANTLRFileStream(srcFileName);
			ModuleLexer lexer = new ModuleLexer(antlrFileStream);
			CommonTokenStream tokens = new CommonTokenStream(lexer);
			ModuleParser parser = new ModuleParser(tokens);
			parser.removeErrorListeners(); // remove error listener
			
			if (bSLL != 0) {
				parser.getInterpreter().setPredictionMode(PredictionMode.SLL);
				parser.setErrorHandler(new BailErrorStrategy());
			}
			
			//long t1 = System.currentTimeMillis();
			ParseTree tree;
			try {
				tree = parser.code();
			}
			catch (ParseCancellationException e) {
				parser.reset();
				parser.getInterpreter().setPredictionMode(PredictionMode.LL);
				parser.setErrorHandler(new DefaultErrorStrategy());
				tree = parser.code();
			}
			//long t2 = System.currentTimeMillis();
			//System.err.println("time: " + (t2 - t1) / 1000.0);
			this._init(parser); // reset before traverse a parse tree
			this.enableSLL = bSLL;
			
			LineNumberReader lnr = new LineNumberReader(new FileReader(new File(srcFileName)));
			while (lnr.skip(Long.MAX_VALUE) > 0);
			this.numLines = lnr.getLineNumber() + 1;
			lnr.close();
			
			this.srcFileName = new String(srcFileName);
			
			ParseTreeWalker.DEFAULT.walk(this, tree);
			
			//System.err.println("before get()");
			//long t3 = System.currentTimeMillis();
			//for (Future<function> future : this.future_list) {
			//	ret.add(future.get());
			//}
			//long t4 = System.currentTimeMillis();
			//System.err.println("time: " + (t4 - t3) / 1000.0);
			//System.err.println("after get()");
			/*
			for (int i = 0; i < job_list.size(); i++) { // singlethread
				JobInstance j = job_list.get(i);
				BodyParser p = new BodyParser();
				p.ParseString(j.string, j.functionInstance, j.line, j.enableSLL);
				ret.add(j.functionInstance);
			}
			*/

		} catch (Exception e) {
			e.printStackTrace();
			//this.executorService.shutdownNow();
			return null;
		}
		//this.executorService.shutdown();
		return this.ret;
	}
	
	@Override
	public void enterEveryRule(ParserRuleContext ctx) {
		int ruleIndex = ctx.getRuleIndex();
		
		if (ruleIndex == TreeParser1.IDX[TreeParser1.FUNCTION_DEF]) {
			this.funcDefFlag = 1;
			this.functionInstance = new function(this.srcFileName);
			this.functionInstance.parentNumLoc = this.numLines;
			this.functionInstance.funcId = this.ret.size() + 1;
			this.functionInstance.lineStart = ctx.getStart().getLine();
			this.functionInstance.lineStop = ctx.getStop().getLine();
		}
		else if (this.funcDefFlag == 0)
			return;
		else if (ruleIndex == TreeParser1.IDX[TreeParser1.FUNCTION_NAME])
			this.funcNameFlag = 1;
		else if (ruleIndex == TreeParser1.IDX[TreeParser1.PARAMETER_NAME])
			this.paramNameFlag = 1;
		else if (ruleIndex == TreeParser1.IDX[TreeParser1.TYPE_NAME])
			this.typeNameFlag = 1;
		else if (ruleIndex == TreeParser1.IDX[TreeParser1.COMPOUND_STMT])
			this.compoundStmtFlag = 1;
	}
	
	@Override
	public void exitEveryRule(ParserRuleContext ctx) {
		int ruleIndex = ctx.getRuleIndex();
		
		if (ruleIndex == TreeParser1.IDX[TreeParser1.FUNCTION_DEF] && this.funcDefFlag != 0) {
			this.ret.add(this.functionInstance);
			this.funcDefFlag = 0;
		}
		else if (ruleIndex == TreeParser1.IDX[TreeParser1.FUNCTION_NAME] && this.funcNameFlag != 0) {
			this.functionInstance.name = this.funcNameStr.toString().trim();
			this.funcNameFlag = 0;
			this.funcNameStr.setLength(0);
		}
		else if (ruleIndex == TreeParser1.IDX[TreeParser1.PARAMETER_NAME] && this.paramNameFlag != 0) {
			this.functionInstance.parameterList.add(this.paramNameStr.toString().trim());
			this.paramNameFlag = 0;
			this.paramNameStr.setLength(0);
		}
		else if (ruleIndex == TreeParser1.IDX[TreeParser1.TYPE_NAME] && this.typeNameFlag != 0) {
			this.functionInstance.dataTypeList.add(this.typeNameStr.toString().trim());
			this.typeNameFlag = 0;
			this.typeNameStr.setLength(0);
		}
		else if (ruleIndex == TreeParser1.IDX[TreeParser1.COMPOUND_STMT] && this.compoundStmtFlag != 0) {
			this.compoundStmtFlag = 0;
			
			CharStream inputStream = ctx.start.getInputStream();
			int start_index = ctx.start.getStopIndex();
			int stop_index = ctx.stop.getStopIndex();
			String string = inputStream.getText(new Interval(start_index + 1, stop_index - 1));
			int line = ctx.start.getLine();
			
			// add function's body
			this.functionInstance.funcBody = string;
			
			//this.job_list.add(new JobInstance(string, this.functionInstance, line, this.enableSLL)); // for singlethread
			//this.future_list.add(
			//	this.executorService.submit(new JobInstance(string, this.functionInstance, line, this.enableSLL))
			//); // for multithread
		}
	}
	
	@Override
	public void visitTerminal(TerminalNode node) {
		if (this.compoundStmtFlag != 0 || this.funcDefFlag == 0)
			return;
		else if (this.funcNameFlag != 0) {
			this.funcNameStr.append(Trees.getNodeText(node, this.ruleNames));
			this.funcNameStr.append(' ');
		}
		else if (this.paramNameFlag != 0) {
			this.paramNameStr.append(Trees.getNodeText(node, this.ruleNames));
			this.paramNameStr.append(' ');
		}
		else if (this.typeNameFlag != 0) {
			this.typeNameStr.append(Trees.getNodeText(node, this.ruleNames));
			this.typeNameStr.append(' ');
		}
	}
	
	@Override
	public void visitErrorNode(ErrorNode node) { }
}
