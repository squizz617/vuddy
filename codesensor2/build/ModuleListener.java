// Generated from Module.g4 by ANTLR 4.5.3

  import java.util.Stack;

import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link ModuleParser}.
 */
public interface ModuleListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link ModuleParser#code}.
	 * @param ctx the parse tree
	 */
	void enterCode(ModuleParser.CodeContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#code}.
	 * @param ctx the parse tree
	 */
	void exitCode(ModuleParser.CodeContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#using_directive}.
	 * @param ctx the parse tree
	 */
	void enterUsing_directive(ModuleParser.Using_directiveContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#using_directive}.
	 * @param ctx the parse tree
	 */
	void exitUsing_directive(ModuleParser.Using_directiveContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterExpr(ModuleParser.ExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitExpr(ModuleParser.ExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#assign_expr}.
	 * @param ctx the parse tree
	 */
	void enterAssign_expr(ModuleParser.Assign_exprContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#assign_expr}.
	 * @param ctx the parse tree
	 */
	void exitAssign_expr(ModuleParser.Assign_exprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code normOr}
	 * labeled alternative in {@link ModuleParser#conditional_expression}.
	 * @param ctx the parse tree
	 */
	void enterNormOr(ModuleParser.NormOrContext ctx);
	/**
	 * Exit a parse tree produced by the {@code normOr}
	 * labeled alternative in {@link ModuleParser#conditional_expression}.
	 * @param ctx the parse tree
	 */
	void exitNormOr(ModuleParser.NormOrContext ctx);
	/**
	 * Enter a parse tree produced by the {@code cndExpr}
	 * labeled alternative in {@link ModuleParser#conditional_expression}.
	 * @param ctx the parse tree
	 */
	void enterCndExpr(ModuleParser.CndExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code cndExpr}
	 * labeled alternative in {@link ModuleParser#conditional_expression}.
	 * @param ctx the parse tree
	 */
	void exitCndExpr(ModuleParser.CndExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#or_expression}.
	 * @param ctx the parse tree
	 */
	void enterOr_expression(ModuleParser.Or_expressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#or_expression}.
	 * @param ctx the parse tree
	 */
	void exitOr_expression(ModuleParser.Or_expressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#and_expression}.
	 * @param ctx the parse tree
	 */
	void enterAnd_expression(ModuleParser.And_expressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#and_expression}.
	 * @param ctx the parse tree
	 */
	void exitAnd_expression(ModuleParser.And_expressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#inclusive_or_expression}.
	 * @param ctx the parse tree
	 */
	void enterInclusive_or_expression(ModuleParser.Inclusive_or_expressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#inclusive_or_expression}.
	 * @param ctx the parse tree
	 */
	void exitInclusive_or_expression(ModuleParser.Inclusive_or_expressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#exclusive_or_expression}.
	 * @param ctx the parse tree
	 */
	void enterExclusive_or_expression(ModuleParser.Exclusive_or_expressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#exclusive_or_expression}.
	 * @param ctx the parse tree
	 */
	void exitExclusive_or_expression(ModuleParser.Exclusive_or_expressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#bit_and_expression}.
	 * @param ctx the parse tree
	 */
	void enterBit_and_expression(ModuleParser.Bit_and_expressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#bit_and_expression}.
	 * @param ctx the parse tree
	 */
	void exitBit_and_expression(ModuleParser.Bit_and_expressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#equality_expression}.
	 * @param ctx the parse tree
	 */
	void enterEquality_expression(ModuleParser.Equality_expressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#equality_expression}.
	 * @param ctx the parse tree
	 */
	void exitEquality_expression(ModuleParser.Equality_expressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#relational_expression}.
	 * @param ctx the parse tree
	 */
	void enterRelational_expression(ModuleParser.Relational_expressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#relational_expression}.
	 * @param ctx the parse tree
	 */
	void exitRelational_expression(ModuleParser.Relational_expressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#shift_expression}.
	 * @param ctx the parse tree
	 */
	void enterShift_expression(ModuleParser.Shift_expressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#shift_expression}.
	 * @param ctx the parse tree
	 */
	void exitShift_expression(ModuleParser.Shift_expressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#additive_expression}.
	 * @param ctx the parse tree
	 */
	void enterAdditive_expression(ModuleParser.Additive_expressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#additive_expression}.
	 * @param ctx the parse tree
	 */
	void exitAdditive_expression(ModuleParser.Additive_expressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#multiplicative_expression}.
	 * @param ctx the parse tree
	 */
	void enterMultiplicative_expression(ModuleParser.Multiplicative_expressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#multiplicative_expression}.
	 * @param ctx the parse tree
	 */
	void exitMultiplicative_expression(ModuleParser.Multiplicative_expressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#cast_expression}.
	 * @param ctx the parse tree
	 */
	void enterCast_expression(ModuleParser.Cast_expressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#cast_expression}.
	 * @param ctx the parse tree
	 */
	void exitCast_expression(ModuleParser.Cast_expressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#cast_target}.
	 * @param ctx the parse tree
	 */
	void enterCast_target(ModuleParser.Cast_targetContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#cast_target}.
	 * @param ctx the parse tree
	 */
	void exitCast_target(ModuleParser.Cast_targetContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#unary_expression}.
	 * @param ctx the parse tree
	 */
	void enterUnary_expression(ModuleParser.Unary_expressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#unary_expression}.
	 * @param ctx the parse tree
	 */
	void exitUnary_expression(ModuleParser.Unary_expressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#new_expression}.
	 * @param ctx the parse tree
	 */
	void enterNew_expression(ModuleParser.New_expressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#new_expression}.
	 * @param ctx the parse tree
	 */
	void exitNew_expression(ModuleParser.New_expressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#unary_op_and_cast_expr}.
	 * @param ctx the parse tree
	 */
	void enterUnary_op_and_cast_expr(ModuleParser.Unary_op_and_cast_exprContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#unary_op_and_cast_expr}.
	 * @param ctx the parse tree
	 */
	void exitUnary_op_and_cast_expr(ModuleParser.Unary_op_and_cast_exprContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#sizeof_expression}.
	 * @param ctx the parse tree
	 */
	void enterSizeof_expression(ModuleParser.Sizeof_expressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#sizeof_expression}.
	 * @param ctx the parse tree
	 */
	void exitSizeof_expression(ModuleParser.Sizeof_expressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#sizeof}.
	 * @param ctx the parse tree
	 */
	void enterSizeof(ModuleParser.SizeofContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#sizeof}.
	 * @param ctx the parse tree
	 */
	void exitSizeof(ModuleParser.SizeofContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#sizeof_operand}.
	 * @param ctx the parse tree
	 */
	void enterSizeof_operand(ModuleParser.Sizeof_operandContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#sizeof_operand}.
	 * @param ctx the parse tree
	 */
	void exitSizeof_operand(ModuleParser.Sizeof_operandContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#sizeof_operand2}.
	 * @param ctx the parse tree
	 */
	void enterSizeof_operand2(ModuleParser.Sizeof_operand2Context ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#sizeof_operand2}.
	 * @param ctx the parse tree
	 */
	void exitSizeof_operand2(ModuleParser.Sizeof_operand2Context ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#inc_dec}.
	 * @param ctx the parse tree
	 */
	void enterInc_dec(ModuleParser.Inc_decContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#inc_dec}.
	 * @param ctx the parse tree
	 */
	void exitInc_dec(ModuleParser.Inc_decContext ctx);
	/**
	 * Enter a parse tree produced by the {@code memberAccess}
	 * labeled alternative in {@link ModuleParser#postfix_expression}.
	 * @param ctx the parse tree
	 */
	void enterMemberAccess(ModuleParser.MemberAccessContext ctx);
	/**
	 * Exit a parse tree produced by the {@code memberAccess}
	 * labeled alternative in {@link ModuleParser#postfix_expression}.
	 * @param ctx the parse tree
	 */
	void exitMemberAccess(ModuleParser.MemberAccessContext ctx);
	/**
	 * Enter a parse tree produced by the {@code incDecOp}
	 * labeled alternative in {@link ModuleParser#postfix_expression}.
	 * @param ctx the parse tree
	 */
	void enterIncDecOp(ModuleParser.IncDecOpContext ctx);
	/**
	 * Exit a parse tree produced by the {@code incDecOp}
	 * labeled alternative in {@link ModuleParser#postfix_expression}.
	 * @param ctx the parse tree
	 */
	void exitIncDecOp(ModuleParser.IncDecOpContext ctx);
	/**
	 * Enter a parse tree produced by the {@code primaryOnly}
	 * labeled alternative in {@link ModuleParser#postfix_expression}.
	 * @param ctx the parse tree
	 */
	void enterPrimaryOnly(ModuleParser.PrimaryOnlyContext ctx);
	/**
	 * Exit a parse tree produced by the {@code primaryOnly}
	 * labeled alternative in {@link ModuleParser#postfix_expression}.
	 * @param ctx the parse tree
	 */
	void exitPrimaryOnly(ModuleParser.PrimaryOnlyContext ctx);
	/**
	 * Enter a parse tree produced by the {@code funcCall}
	 * labeled alternative in {@link ModuleParser#postfix_expression}.
	 * @param ctx the parse tree
	 */
	void enterFuncCall(ModuleParser.FuncCallContext ctx);
	/**
	 * Exit a parse tree produced by the {@code funcCall}
	 * labeled alternative in {@link ModuleParser#postfix_expression}.
	 * @param ctx the parse tree
	 */
	void exitFuncCall(ModuleParser.FuncCallContext ctx);
	/**
	 * Enter a parse tree produced by the {@code arrayIndexing}
	 * labeled alternative in {@link ModuleParser#postfix_expression}.
	 * @param ctx the parse tree
	 */
	void enterArrayIndexing(ModuleParser.ArrayIndexingContext ctx);
	/**
	 * Exit a parse tree produced by the {@code arrayIndexing}
	 * labeled alternative in {@link ModuleParser#postfix_expression}.
	 * @param ctx the parse tree
	 */
	void exitArrayIndexing(ModuleParser.ArrayIndexingContext ctx);
	/**
	 * Enter a parse tree produced by the {@code ptrMemberAccess}
	 * labeled alternative in {@link ModuleParser#postfix_expression}.
	 * @param ctx the parse tree
	 */
	void enterPtrMemberAccess(ModuleParser.PtrMemberAccessContext ctx);
	/**
	 * Exit a parse tree produced by the {@code ptrMemberAccess}
	 * labeled alternative in {@link ModuleParser#postfix_expression}.
	 * @param ctx the parse tree
	 */
	void exitPtrMemberAccess(ModuleParser.PtrMemberAccessContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#function_argument_list}.
	 * @param ctx the parse tree
	 */
	void enterFunction_argument_list(ModuleParser.Function_argument_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#function_argument_list}.
	 * @param ctx the parse tree
	 */
	void exitFunction_argument_list(ModuleParser.Function_argument_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#function_argument}.
	 * @param ctx the parse tree
	 */
	void enterFunction_argument(ModuleParser.Function_argumentContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#function_argument}.
	 * @param ctx the parse tree
	 */
	void exitFunction_argument(ModuleParser.Function_argumentContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#primary_expression}.
	 * @param ctx the parse tree
	 */
	void enterPrimary_expression(ModuleParser.Primary_expressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#primary_expression}.
	 * @param ctx the parse tree
	 */
	void exitPrimary_expression(ModuleParser.Primary_expressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#unary_operator}.
	 * @param ctx the parse tree
	 */
	void enterUnary_operator(ModuleParser.Unary_operatorContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#unary_operator}.
	 * @param ctx the parse tree
	 */
	void exitUnary_operator(ModuleParser.Unary_operatorContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#relational_operator}.
	 * @param ctx the parse tree
	 */
	void enterRelational_operator(ModuleParser.Relational_operatorContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#relational_operator}.
	 * @param ctx the parse tree
	 */
	void exitRelational_operator(ModuleParser.Relational_operatorContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#constant}.
	 * @param ctx the parse tree
	 */
	void enterConstant(ModuleParser.ConstantContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#constant}.
	 * @param ctx the parse tree
	 */
	void exitConstant(ModuleParser.ConstantContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#function_decl_specifiers}.
	 * @param ctx the parse tree
	 */
	void enterFunction_decl_specifiers(ModuleParser.Function_decl_specifiersContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#function_decl_specifiers}.
	 * @param ctx the parse tree
	 */
	void exitFunction_decl_specifiers(ModuleParser.Function_decl_specifiersContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#ptr_operator}.
	 * @param ctx the parse tree
	 */
	void enterPtr_operator(ModuleParser.Ptr_operatorContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#ptr_operator}.
	 * @param ctx the parse tree
	 */
	void exitPtr_operator(ModuleParser.Ptr_operatorContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#access_specifier}.
	 * @param ctx the parse tree
	 */
	void enterAccess_specifier(ModuleParser.Access_specifierContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#access_specifier}.
	 * @param ctx the parse tree
	 */
	void exitAccess_specifier(ModuleParser.Access_specifierContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#operator}.
	 * @param ctx the parse tree
	 */
	void enterOperator(ModuleParser.OperatorContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#operator}.
	 * @param ctx the parse tree
	 */
	void exitOperator(ModuleParser.OperatorContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#assignment_operator}.
	 * @param ctx the parse tree
	 */
	void enterAssignment_operator(ModuleParser.Assignment_operatorContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#assignment_operator}.
	 * @param ctx the parse tree
	 */
	void exitAssignment_operator(ModuleParser.Assignment_operatorContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#equality_operator}.
	 * @param ctx the parse tree
	 */
	void enterEquality_operator(ModuleParser.Equality_operatorContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#equality_operator}.
	 * @param ctx the parse tree
	 */
	void exitEquality_operator(ModuleParser.Equality_operatorContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#template_decl_start}.
	 * @param ctx the parse tree
	 */
	void enterTemplate_decl_start(ModuleParser.Template_decl_startContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#template_decl_start}.
	 * @param ctx the parse tree
	 */
	void exitTemplate_decl_start(ModuleParser.Template_decl_startContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#template_param_list}.
	 * @param ctx the parse tree
	 */
	void enterTemplate_param_list(ModuleParser.Template_param_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#template_param_list}.
	 * @param ctx the parse tree
	 */
	void exitTemplate_param_list(ModuleParser.Template_param_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#no_brackets}.
	 * @param ctx the parse tree
	 */
	void enterNo_brackets(ModuleParser.No_bracketsContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#no_brackets}.
	 * @param ctx the parse tree
	 */
	void exitNo_brackets(ModuleParser.No_bracketsContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#no_brackets_curlies_or_squares}.
	 * @param ctx the parse tree
	 */
	void enterNo_brackets_curlies_or_squares(ModuleParser.No_brackets_curlies_or_squaresContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#no_brackets_curlies_or_squares}.
	 * @param ctx the parse tree
	 */
	void exitNo_brackets_curlies_or_squares(ModuleParser.No_brackets_curlies_or_squaresContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#no_brackets_or_semicolon}.
	 * @param ctx the parse tree
	 */
	void enterNo_brackets_or_semicolon(ModuleParser.No_brackets_or_semicolonContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#no_brackets_or_semicolon}.
	 * @param ctx the parse tree
	 */
	void exitNo_brackets_or_semicolon(ModuleParser.No_brackets_or_semicolonContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#no_angle_brackets_or_brackets}.
	 * @param ctx the parse tree
	 */
	void enterNo_angle_brackets_or_brackets(ModuleParser.No_angle_brackets_or_bracketsContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#no_angle_brackets_or_brackets}.
	 * @param ctx the parse tree
	 */
	void exitNo_angle_brackets_or_brackets(ModuleParser.No_angle_brackets_or_bracketsContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#no_curlies}.
	 * @param ctx the parse tree
	 */
	void enterNo_curlies(ModuleParser.No_curliesContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#no_curlies}.
	 * @param ctx the parse tree
	 */
	void exitNo_curlies(ModuleParser.No_curliesContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#no_squares}.
	 * @param ctx the parse tree
	 */
	void enterNo_squares(ModuleParser.No_squaresContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#no_squares}.
	 * @param ctx the parse tree
	 */
	void exitNo_squares(ModuleParser.No_squaresContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#no_squares_or_semicolon}.
	 * @param ctx the parse tree
	 */
	void enterNo_squares_or_semicolon(ModuleParser.No_squares_or_semicolonContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#no_squares_or_semicolon}.
	 * @param ctx the parse tree
	 */
	void exitNo_squares_or_semicolon(ModuleParser.No_squares_or_semicolonContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#no_comma_or_semicolon}.
	 * @param ctx the parse tree
	 */
	void enterNo_comma_or_semicolon(ModuleParser.No_comma_or_semicolonContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#no_comma_or_semicolon}.
	 * @param ctx the parse tree
	 */
	void exitNo_comma_or_semicolon(ModuleParser.No_comma_or_semicolonContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#assign_water}.
	 * @param ctx the parse tree
	 */
	void enterAssign_water(ModuleParser.Assign_waterContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#assign_water}.
	 * @param ctx the parse tree
	 */
	void exitAssign_water(ModuleParser.Assign_waterContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#assign_water_l2}.
	 * @param ctx the parse tree
	 */
	void enterAssign_water_l2(ModuleParser.Assign_water_l2Context ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#assign_water_l2}.
	 * @param ctx the parse tree
	 */
	void exitAssign_water_l2(ModuleParser.Assign_water_l2Context ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#water}.
	 * @param ctx the parse tree
	 */
	void enterWater(ModuleParser.WaterContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#water}.
	 * @param ctx the parse tree
	 */
	void exitWater(ModuleParser.WaterContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#function_def}.
	 * @param ctx the parse tree
	 */
	void enterFunction_def(ModuleParser.Function_defContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#function_def}.
	 * @param ctx the parse tree
	 */
	void exitFunction_def(ModuleParser.Function_defContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#return_type}.
	 * @param ctx the parse tree
	 */
	void enterReturn_type(ModuleParser.Return_typeContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#return_type}.
	 * @param ctx the parse tree
	 */
	void exitReturn_type(ModuleParser.Return_typeContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#function_param_list}.
	 * @param ctx the parse tree
	 */
	void enterFunction_param_list(ModuleParser.Function_param_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#function_param_list}.
	 * @param ctx the parse tree
	 */
	void exitFunction_param_list(ModuleParser.Function_param_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#parameter_decl_clause}.
	 * @param ctx the parse tree
	 */
	void enterParameter_decl_clause(ModuleParser.Parameter_decl_clauseContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#parameter_decl_clause}.
	 * @param ctx the parse tree
	 */
	void exitParameter_decl_clause(ModuleParser.Parameter_decl_clauseContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#parameter_decl}.
	 * @param ctx the parse tree
	 */
	void enterParameter_decl(ModuleParser.Parameter_declContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#parameter_decl}.
	 * @param ctx the parse tree
	 */
	void exitParameter_decl(ModuleParser.Parameter_declContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#parameter_id}.
	 * @param ctx the parse tree
	 */
	void enterParameter_id(ModuleParser.Parameter_idContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#parameter_id}.
	 * @param ctx the parse tree
	 */
	void exitParameter_id(ModuleParser.Parameter_idContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#compound_statement}.
	 * @param ctx the parse tree
	 */
	void enterCompound_statement(ModuleParser.Compound_statementContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#compound_statement}.
	 * @param ctx the parse tree
	 */
	void exitCompound_statement(ModuleParser.Compound_statementContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#ctor_list}.
	 * @param ctx the parse tree
	 */
	void enterCtor_list(ModuleParser.Ctor_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#ctor_list}.
	 * @param ctx the parse tree
	 */
	void exitCtor_list(ModuleParser.Ctor_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#ctor_initializer}.
	 * @param ctx the parse tree
	 */
	void enterCtor_initializer(ModuleParser.Ctor_initializerContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#ctor_initializer}.
	 * @param ctx the parse tree
	 */
	void exitCtor_initializer(ModuleParser.Ctor_initializerContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#initializer_id}.
	 * @param ctx the parse tree
	 */
	void enterInitializer_id(ModuleParser.Initializer_idContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#initializer_id}.
	 * @param ctx the parse tree
	 */
	void exitInitializer_id(ModuleParser.Initializer_idContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#ctor_expr}.
	 * @param ctx the parse tree
	 */
	void enterCtor_expr(ModuleParser.Ctor_exprContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#ctor_expr}.
	 * @param ctx the parse tree
	 */
	void exitCtor_expr(ModuleParser.Ctor_exprContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#function_name}.
	 * @param ctx the parse tree
	 */
	void enterFunction_name(ModuleParser.Function_nameContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#function_name}.
	 * @param ctx the parse tree
	 */
	void exitFunction_name(ModuleParser.Function_nameContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#exception_specification}.
	 * @param ctx the parse tree
	 */
	void enterException_specification(ModuleParser.Exception_specificationContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#exception_specification}.
	 * @param ctx the parse tree
	 */
	void exitException_specification(ModuleParser.Exception_specificationContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#type_id_list}.
	 * @param ctx the parse tree
	 */
	void enterType_id_list(ModuleParser.Type_id_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#type_id_list}.
	 * @param ctx the parse tree
	 */
	void exitType_id_list(ModuleParser.Type_id_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#statements}.
	 * @param ctx the parse tree
	 */
	void enterStatements(ModuleParser.StatementsContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#statements}.
	 * @param ctx the parse tree
	 */
	void exitStatements(ModuleParser.StatementsContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterStatement(ModuleParser.StatementContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitStatement(ModuleParser.StatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#pre_opener}.
	 * @param ctx the parse tree
	 */
	void enterPre_opener(ModuleParser.Pre_openerContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#pre_opener}.
	 * @param ctx the parse tree
	 */
	void exitPre_opener(ModuleParser.Pre_openerContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#pre_else}.
	 * @param ctx the parse tree
	 */
	void enterPre_else(ModuleParser.Pre_elseContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#pre_else}.
	 * @param ctx the parse tree
	 */
	void exitPre_else(ModuleParser.Pre_elseContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#pre_closer}.
	 * @param ctx the parse tree
	 */
	void enterPre_closer(ModuleParser.Pre_closerContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#pre_closer}.
	 * @param ctx the parse tree
	 */
	void exitPre_closer(ModuleParser.Pre_closerContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#opening_curly}.
	 * @param ctx the parse tree
	 */
	void enterOpening_curly(ModuleParser.Opening_curlyContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#opening_curly}.
	 * @param ctx the parse tree
	 */
	void exitOpening_curly(ModuleParser.Opening_curlyContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#closing_curly}.
	 * @param ctx the parse tree
	 */
	void enterClosing_curly(ModuleParser.Closing_curlyContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#closing_curly}.
	 * @param ctx the parse tree
	 */
	void exitClosing_curly(ModuleParser.Closing_curlyContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#block_starter}.
	 * @param ctx the parse tree
	 */
	void enterBlock_starter(ModuleParser.Block_starterContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#block_starter}.
	 * @param ctx the parse tree
	 */
	void exitBlock_starter(ModuleParser.Block_starterContext ctx);
	/**
	 * Enter a parse tree produced by the {@code Try_statement}
	 * labeled alternative in {@link ModuleParser#selection_or_iteration}.
	 * @param ctx the parse tree
	 */
	void enterTry_statement(ModuleParser.Try_statementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code Try_statement}
	 * labeled alternative in {@link ModuleParser#selection_or_iteration}.
	 * @param ctx the parse tree
	 */
	void exitTry_statement(ModuleParser.Try_statementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code Catch_statement}
	 * labeled alternative in {@link ModuleParser#selection_or_iteration}.
	 * @param ctx the parse tree
	 */
	void enterCatch_statement(ModuleParser.Catch_statementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code Catch_statement}
	 * labeled alternative in {@link ModuleParser#selection_or_iteration}.
	 * @param ctx the parse tree
	 */
	void exitCatch_statement(ModuleParser.Catch_statementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code If_statement}
	 * labeled alternative in {@link ModuleParser#selection_or_iteration}.
	 * @param ctx the parse tree
	 */
	void enterIf_statement(ModuleParser.If_statementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code If_statement}
	 * labeled alternative in {@link ModuleParser#selection_or_iteration}.
	 * @param ctx the parse tree
	 */
	void exitIf_statement(ModuleParser.If_statementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code Else_statement}
	 * labeled alternative in {@link ModuleParser#selection_or_iteration}.
	 * @param ctx the parse tree
	 */
	void enterElse_statement(ModuleParser.Else_statementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code Else_statement}
	 * labeled alternative in {@link ModuleParser#selection_or_iteration}.
	 * @param ctx the parse tree
	 */
	void exitElse_statement(ModuleParser.Else_statementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code Switch_statement}
	 * labeled alternative in {@link ModuleParser#selection_or_iteration}.
	 * @param ctx the parse tree
	 */
	void enterSwitch_statement(ModuleParser.Switch_statementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code Switch_statement}
	 * labeled alternative in {@link ModuleParser#selection_or_iteration}.
	 * @param ctx the parse tree
	 */
	void exitSwitch_statement(ModuleParser.Switch_statementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code For_statement}
	 * labeled alternative in {@link ModuleParser#selection_or_iteration}.
	 * @param ctx the parse tree
	 */
	void enterFor_statement(ModuleParser.For_statementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code For_statement}
	 * labeled alternative in {@link ModuleParser#selection_or_iteration}.
	 * @param ctx the parse tree
	 */
	void exitFor_statement(ModuleParser.For_statementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code Do_statement}
	 * labeled alternative in {@link ModuleParser#selection_or_iteration}.
	 * @param ctx the parse tree
	 */
	void enterDo_statement(ModuleParser.Do_statementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code Do_statement}
	 * labeled alternative in {@link ModuleParser#selection_or_iteration}.
	 * @param ctx the parse tree
	 */
	void exitDo_statement(ModuleParser.Do_statementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code While_statement}
	 * labeled alternative in {@link ModuleParser#selection_or_iteration}.
	 * @param ctx the parse tree
	 */
	void enterWhile_statement(ModuleParser.While_statementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code While_statement}
	 * labeled alternative in {@link ModuleParser#selection_or_iteration}.
	 * @param ctx the parse tree
	 */
	void exitWhile_statement(ModuleParser.While_statementContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#do_statement1}.
	 * @param ctx the parse tree
	 */
	void enterDo_statement1(ModuleParser.Do_statement1Context ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#do_statement1}.
	 * @param ctx the parse tree
	 */
	void exitDo_statement1(ModuleParser.Do_statement1Context ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#for_init_statement}.
	 * @param ctx the parse tree
	 */
	void enterFor_init_statement(ModuleParser.For_init_statementContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#for_init_statement}.
	 * @param ctx the parse tree
	 */
	void exitFor_init_statement(ModuleParser.For_init_statementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code breakStatement}
	 * labeled alternative in {@link ModuleParser#jump_statement}.
	 * @param ctx the parse tree
	 */
	void enterBreakStatement(ModuleParser.BreakStatementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code breakStatement}
	 * labeled alternative in {@link ModuleParser#jump_statement}.
	 * @param ctx the parse tree
	 */
	void exitBreakStatement(ModuleParser.BreakStatementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code continueStatement}
	 * labeled alternative in {@link ModuleParser#jump_statement}.
	 * @param ctx the parse tree
	 */
	void enterContinueStatement(ModuleParser.ContinueStatementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code continueStatement}
	 * labeled alternative in {@link ModuleParser#jump_statement}.
	 * @param ctx the parse tree
	 */
	void exitContinueStatement(ModuleParser.ContinueStatementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code gotoStatement}
	 * labeled alternative in {@link ModuleParser#jump_statement}.
	 * @param ctx the parse tree
	 */
	void enterGotoStatement(ModuleParser.GotoStatementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code gotoStatement}
	 * labeled alternative in {@link ModuleParser#jump_statement}.
	 * @param ctx the parse tree
	 */
	void exitGotoStatement(ModuleParser.GotoStatementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code returnStatement}
	 * labeled alternative in {@link ModuleParser#jump_statement}.
	 * @param ctx the parse tree
	 */
	void enterReturnStatement(ModuleParser.ReturnStatementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code returnStatement}
	 * labeled alternative in {@link ModuleParser#jump_statement}.
	 * @param ctx the parse tree
	 */
	void exitReturnStatement(ModuleParser.ReturnStatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#label}.
	 * @param ctx the parse tree
	 */
	void enterLabel(ModuleParser.LabelContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#label}.
	 * @param ctx the parse tree
	 */
	void exitLabel(ModuleParser.LabelContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#expr_statement}.
	 * @param ctx the parse tree
	 */
	void enterExpr_statement(ModuleParser.Expr_statementContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#expr_statement}.
	 * @param ctx the parse tree
	 */
	void exitExpr_statement(ModuleParser.Expr_statementContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#condition}.
	 * @param ctx the parse tree
	 */
	void enterCondition(ModuleParser.ConditionContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#condition}.
	 * @param ctx the parse tree
	 */
	void exitCondition(ModuleParser.ConditionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code initDeclWithCall}
	 * labeled alternative in {@link ModuleParser#init_declarator}.
	 * @param ctx the parse tree
	 */
	void enterInitDeclWithCall(ModuleParser.InitDeclWithCallContext ctx);
	/**
	 * Exit a parse tree produced by the {@code initDeclWithCall}
	 * labeled alternative in {@link ModuleParser#init_declarator}.
	 * @param ctx the parse tree
	 */
	void exitInitDeclWithCall(ModuleParser.InitDeclWithCallContext ctx);
	/**
	 * Enter a parse tree produced by the {@code initDeclWithAssign}
	 * labeled alternative in {@link ModuleParser#init_declarator}.
	 * @param ctx the parse tree
	 */
	void enterInitDeclWithAssign(ModuleParser.InitDeclWithAssignContext ctx);
	/**
	 * Exit a parse tree produced by the {@code initDeclWithAssign}
	 * labeled alternative in {@link ModuleParser#init_declarator}.
	 * @param ctx the parse tree
	 */
	void exitInitDeclWithAssign(ModuleParser.InitDeclWithAssignContext ctx);
	/**
	 * Enter a parse tree produced by the {@code initDeclSimple}
	 * labeled alternative in {@link ModuleParser#init_declarator}.
	 * @param ctx the parse tree
	 */
	void enterInitDeclSimple(ModuleParser.InitDeclSimpleContext ctx);
	/**
	 * Exit a parse tree produced by the {@code initDeclSimple}
	 * labeled alternative in {@link ModuleParser#init_declarator}.
	 * @param ctx the parse tree
	 */
	void exitInitDeclSimple(ModuleParser.InitDeclSimpleContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#declarator}.
	 * @param ctx the parse tree
	 */
	void enterDeclarator(ModuleParser.DeclaratorContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#declarator}.
	 * @param ctx the parse tree
	 */
	void exitDeclarator(ModuleParser.DeclaratorContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#type_suffix}.
	 * @param ctx the parse tree
	 */
	void enterType_suffix(ModuleParser.Type_suffixContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#type_suffix}.
	 * @param ctx the parse tree
	 */
	void exitType_suffix(ModuleParser.Type_suffixContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#simple_decl}.
	 * @param ctx the parse tree
	 */
	void enterSimple_decl(ModuleParser.Simple_declContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#simple_decl}.
	 * @param ctx the parse tree
	 */
	void exitSimple_decl(ModuleParser.Simple_declContext ctx);
	/**
	 * Enter a parse tree produced by the {@code declByClass}
	 * labeled alternative in {@link ModuleParser#var_decl}.
	 * @param ctx the parse tree
	 */
	void enterDeclByClass(ModuleParser.DeclByClassContext ctx);
	/**
	 * Exit a parse tree produced by the {@code declByClass}
	 * labeled alternative in {@link ModuleParser#var_decl}.
	 * @param ctx the parse tree
	 */
	void exitDeclByClass(ModuleParser.DeclByClassContext ctx);
	/**
	 * Enter a parse tree produced by the {@code declByType}
	 * labeled alternative in {@link ModuleParser#var_decl}.
	 * @param ctx the parse tree
	 */
	void enterDeclByType(ModuleParser.DeclByTypeContext ctx);
	/**
	 * Exit a parse tree produced by the {@code declByType}
	 * labeled alternative in {@link ModuleParser#var_decl}.
	 * @param ctx the parse tree
	 */
	void exitDeclByType(ModuleParser.DeclByTypeContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#init_declarator_list}.
	 * @param ctx the parse tree
	 */
	void enterInit_declarator_list(ModuleParser.Init_declarator_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#init_declarator_list}.
	 * @param ctx the parse tree
	 */
	void exitInit_declarator_list(ModuleParser.Init_declarator_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#initializer}.
	 * @param ctx the parse tree
	 */
	void enterInitializer(ModuleParser.InitializerContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#initializer}.
	 * @param ctx the parse tree
	 */
	void exitInitializer(ModuleParser.InitializerContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#initializer_list}.
	 * @param ctx the parse tree
	 */
	void enterInitializer_list(ModuleParser.Initializer_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#initializer_list}.
	 * @param ctx the parse tree
	 */
	void exitInitializer_list(ModuleParser.Initializer_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#class_def}.
	 * @param ctx the parse tree
	 */
	void enterClass_def(ModuleParser.Class_defContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#class_def}.
	 * @param ctx the parse tree
	 */
	void exitClass_def(ModuleParser.Class_defContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#class_name}.
	 * @param ctx the parse tree
	 */
	void enterClass_name(ModuleParser.Class_nameContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#class_name}.
	 * @param ctx the parse tree
	 */
	void exitClass_name(ModuleParser.Class_nameContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#base_classes}.
	 * @param ctx the parse tree
	 */
	void enterBase_classes(ModuleParser.Base_classesContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#base_classes}.
	 * @param ctx the parse tree
	 */
	void exitBase_classes(ModuleParser.Base_classesContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#base_class}.
	 * @param ctx the parse tree
	 */
	void enterBase_class(ModuleParser.Base_classContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#base_class}.
	 * @param ctx the parse tree
	 */
	void exitBase_class(ModuleParser.Base_classContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#type_name}.
	 * @param ctx the parse tree
	 */
	void enterType_name(ModuleParser.Type_nameContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#type_name}.
	 * @param ctx the parse tree
	 */
	void exitType_name(ModuleParser.Type_nameContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#base_type}.
	 * @param ctx the parse tree
	 */
	void enterBase_type(ModuleParser.Base_typeContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#base_type}.
	 * @param ctx the parse tree
	 */
	void exitBase_type(ModuleParser.Base_typeContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#param_decl_specifiers}.
	 * @param ctx the parse tree
	 */
	void enterParam_decl_specifiers(ModuleParser.Param_decl_specifiersContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#param_decl_specifiers}.
	 * @param ctx the parse tree
	 */
	void exitParam_decl_specifiers(ModuleParser.Param_decl_specifiersContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#parameter_name}.
	 * @param ctx the parse tree
	 */
	void enterParameter_name(ModuleParser.Parameter_nameContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#parameter_name}.
	 * @param ctx the parse tree
	 */
	void exitParameter_name(ModuleParser.Parameter_nameContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#param_type_list}.
	 * @param ctx the parse tree
	 */
	void enterParam_type_list(ModuleParser.Param_type_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#param_type_list}.
	 * @param ctx the parse tree
	 */
	void exitParam_type_list(ModuleParser.Param_type_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#param_type}.
	 * @param ctx the parse tree
	 */
	void enterParam_type(ModuleParser.Param_typeContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#param_type}.
	 * @param ctx the parse tree
	 */
	void exitParam_type(ModuleParser.Param_typeContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#param_type_id}.
	 * @param ctx the parse tree
	 */
	void enterParam_type_id(ModuleParser.Param_type_idContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#param_type_id}.
	 * @param ctx the parse tree
	 */
	void exitParam_type_id(ModuleParser.Param_type_idContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#identifier}.
	 * @param ctx the parse tree
	 */
	void enterIdentifier(ModuleParser.IdentifierContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#identifier}.
	 * @param ctx the parse tree
	 */
	void exitIdentifier(ModuleParser.IdentifierContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#number}.
	 * @param ctx the parse tree
	 */
	void enterNumber(ModuleParser.NumberContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#number}.
	 * @param ctx the parse tree
	 */
	void exitNumber(ModuleParser.NumberContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#ptrs}.
	 * @param ctx the parse tree
	 */
	void enterPtrs(ModuleParser.PtrsContext ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#ptrs}.
	 * @param ctx the parse tree
	 */
	void exitPtrs(ModuleParser.PtrsContext ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#assign_expr_w_}.
	 * @param ctx the parse tree
	 */
	void enterAssign_expr_w_(ModuleParser.Assign_expr_w_Context ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#assign_expr_w_}.
	 * @param ctx the parse tree
	 */
	void exitAssign_expr_w_(ModuleParser.Assign_expr_w_Context ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#assign_expr_w__l2}.
	 * @param ctx the parse tree
	 */
	void enterAssign_expr_w__l2(ModuleParser.Assign_expr_w__l2Context ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#assign_expr_w__l2}.
	 * @param ctx the parse tree
	 */
	void exitAssign_expr_w__l2(ModuleParser.Assign_expr_w__l2Context ctx);
	/**
	 * Enter a parse tree produced by {@link ModuleParser#constant_expr_w_}.
	 * @param ctx the parse tree
	 */
	void enterConstant_expr_w_(ModuleParser.Constant_expr_w_Context ctx);
	/**
	 * Exit a parse tree produced by {@link ModuleParser#constant_expr_w_}.
	 * @param ctx the parse tree
	 */
	void exitConstant_expr_w_(ModuleParser.Constant_expr_w_Context ctx);
}