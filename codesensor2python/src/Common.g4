grammar Common;
/*
@header{
  import java.util.Stack;
}
*/

@parser::members
{
def skipToEndOfObject(self):
    CurlyStack = []
    t = self._input.LA(1)

    while (t != self.EOF and not (len(CurlyStack) == 0 and t == self.CLOSING_CURLY)):
        if t == self.PRE_ELSE:
            ifdefStack = []
            self.consume()
            t = self._input.LA(1)
            
            while (t != self.EOF and not (len(ifdefStack) == 0 and t == self.PRE_ENDIF)):
                if t == self.PRE_IF:
                    ifdefStack.append(1)
                elif t == self.PRE_ENDIF:
                    ifdefStack.pop()
                
                self.consume()
                t = self._input.LA(1)
        
        if t == self.OPENING_CURLY:
            CurlyStack.append(1)
        elif t == self.CLOSING_CURLY:
            CurlyStack.pop()
        
        self.consume()
        t = self._input.LA(1)
    
    if t != self.EOF:
        self.consume()


# this should go into FunctionGrammar but ANTLR fails
# to join the parser::members-section on inclusion
def preProcSkipToEnd(self):
    CurlyStack = []
    t = self._input.LA(1)
    
    while (t != self.EOF and not (len(CurlyStack) == 0 and t == self.PRE_ENDIF)):
        if t == self.PRE_IF:
            CurlyStack.append(1)
        elif t == self.PRE_ENDIF:
            CurlyStack.pop()
        
        self.consume()
        t = self._input.LA(1)
    
    if t == self.EOF:
        self.consume()
}

unary_operator : '&' | '*' | '+'| '-' | '~' | '!';
relational_operator: ('<'|'>'|'<='|'>=');

constant
    :   HEX_LITERAL
    |   OCTAL_LITERAL
    |   DECIMAL_LITERAL
	|	STRING
    |   CHAR
    |   FLOATING_POINT_LITERAL
    ;

// keywords & operators

function_decl_specifiers: ('inline' | 'virtual' | 'explicit' | 'friend' | 'static');
ptr_operator: ('*' | '&');

access_specifier: ('public' | 'private' | 'protected');

operator: (('new' | 'delete' ) ('[' ']')?)
  | '+' | '-' | '*' | '/' | '%' |'^' | '&' | '|' | '~'
  | '!' | '=' | '<' | '>' | '+=' | '-=' | '*='
  | '/=' | '%=' | '^=' | '&=' | '|=' | '>>'
  |'<<'| '>>=' | '<<=' | '==' | '!='
  | '<=' | '>=' | '&&' | '||' | '++' | '--'
  | ',' | '->*' | '->' | '(' ')' | '[' ']'
  ;

assignment_operator: '=' | '*=' | '/=' | '%=' | '+=' | '-=' | '<<=' | '>>=' | '&=' | '^=' | '|='; 
equality_operator: ('=='| '!=');

template_decl_start : TEMPLATE '<' template_param_list '>';


// template water
template_param_list : (('<' template_param_list '>') |
                       ('(' template_param_list ')') | 
                       no_angle_brackets_or_brackets)+
;

// water

no_brackets: ~('(' | ')');
no_brackets_curlies_or_squares: ~('(' | ')' | '{' | '}' | '[' | ']');
no_brackets_or_semicolon: ~('(' | ')' | ';');
no_angle_brackets_or_brackets : ~('<' | '>' | '(' | ')');
no_curlies: ~('{' | '}');
no_squares: ~('[' | ']');
no_squares_or_semicolon: ~('[' | ']' | ';');
no_comma_or_semicolon: ~(',' | ';');

assign_water: ~('(' | ')' | '{' | '}' | '[' | ']' | ';' | ',');
assign_water_l2: ~('(' | ')' | '{' | '}' | '[' | ']');

water: .;
