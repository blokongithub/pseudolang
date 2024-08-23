from sly import Parser
from pseudolexer import PseudoCodeLexer

class PseudoCodeParser(Parser):
    tokens = PseudoCodeLexer.tokens

    precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'NOT'),
        ('left', '<', '>', '≤', '≥', '≠', '='),
        ('left', '+', '-'),
        ('left', '*', '/', 'MOD', 'DIV'),
        ('left', '(', '[', ','),
    )

    @_('statement_list')
    def program(self, p):
        return {
            "type": "program",
            "body": p.statement_list
        }

    @_('statement_list statement')
    def statement_list(self, p):
        return p.statement_list + [p.statement]

    @_('statement')
    def statement_list(self, p):
        return [p.statement]

    @_('assignment',
       'list_assignment',
       'list_call',
       'listvalue_assignment',
       'if_statement',
       'while_loop',
       'repeat_until_loop',
       'for_loop',
       'output_statement',
       'input_statement',
       'subroutine_declaration',
       'subroutine_call',
       'expression_statement',
       'constant_declaration',
       'break_statement',
       'return_statement')
    def statement(self, p):
        return p[0]

    @_('IDENTIFIER ASSIGN expression')
    def assignment(self, p):
        return {
            "type": "assign",
            "target": p.IDENTIFIER,
            "value": p.expression
        }
    @_('IDENTIFIER "[" expression "]" ASSIGN expression')
    def listvalue_assignment(self, p):
        return {
            "type": "listvalue_assign",
            "target": p.IDENTIFIER,
            "index": p.expression0,
            "value": p.expression1
        }
    
    @_('empty')
    def list_assignment(self, p):
        return []

    
    @_('expression_list "," expression')
    def expression_list(self, p):
        return p.expression_list + [p.expression]
    
    @_('IDENTIFIER ASSIGN "[" expression_list "]"')
    def list_assignment(self, p):
        return {
            "type": "list_assign",
            "target": p.IDENTIFIER,
            "value": p.expression_list
        }
    
    @_('IDENTIFIER ASSIGN subroutine_call')
    def assignment(self, p):
        return {
            "type": "assign",
            "target": p.IDENTIFIER,
            "value": p.subroutine_call
        }

    @_('IDENTIFIER ASSIGN USERINPUT')
    def assignment(self, p):
        return {
            "type": "userinput",
            "target": p.IDENTIFIER,
        }

    @_('IF expression THEN statement_list else_if_list else_statement ENDIF')
    def if_statement(self, p):
        return {
            "type": "if_elseif",
            "condition": p.expression,
            "then": p.statement_list,
            "else_if": p.else_if_list,
            "else": p.else_statement
        }

    @_('else_if_list ELSE IF expression THEN statement_list')
    def else_if_list(self, p):
        return p.else_if_list + [{
            "condition": p.expression,
            "then": p.statement_list
        }]

    @_('empty')
    def else_if_list(self, p):
        return []

    @_('ELSE IF expression THEN statement_list')
    def else_if_clause(self, p):
        return [(p.expression, p.statement_list)]

    @_('ELSE statement_list')
    def else_statement(self, p):
        return p.statement_list

    @_('empty')
    def else_statement(self, p):
        return None

    @_('')
    def empty(self, p):
        return None

    @_('WHILE expression DO statement_list ENDWHILE')
    def while_loop(self, p):
        return {
            "type": "while",
            "condition": p.expression,
            "body": p.statement_list
        }

    @_('REPEAT statement_list UNTIL expression')
    def repeat_until_loop(self, p):
        return {
            "type": "repeat_until",
            "body": p.statement_list,
            "condition": p.expression
        }
    
    @_('BREAK')
    def break_statement(self, p):
        return {
            "type": "break"
        }
        
    @_('RETURN expression')
    def return_statement(self, p):
        return {
            "type": "return",
            "value": p.expression
        }

    @_('RETURN')
    def return_statement(self, p):
        return {
            "type": "return",
            "value": None
        }

    @_('FOR IDENTIFIER IN IDENTIFIER statement_list ENDFOR')
    def for_loop(self, p):
        return {
            "type": "for",
            "item": p.IDENTIFIER0,
            "list": p.IDENTIFIER1,
            "body": p.statement_list
        }

    @_('FOR IDENTIFIER ASSIGN expression TO expression STEP expression statement_list ENDFOR')
    def for_loop(self, p):
        return {
            "type": "for",
            "variable": p.IDENTIFIER,
            "start": p.expression0,
            "end": p.expression1,
            "step": p.expression2,
            "body": p.statement_list
        }

    @_('FOR IDENTIFIER ASSIGN expression TO expression statement_list ENDFOR')
    def for_loop(self, p):
        return {
            "type": "for",
            "variable": p.IDENTIFIER,
            "start": p.expression0,
            "end": p.expression1,
            "step": {"type": "int", "value": 1},
            "body": p.statement_list
        }

    @_('OUTPUT expression_list')
    def output_statement(self, p):
        return {
            "type": "output",
            "value": p.expression_list
        }

    @_('USERINPUT IDENTIFIER')
    def input_statement(self, p):
        return {
            "type": "input",
            "target": p.IDENTIFIER
        }

    @_('SUBROUTINE IDENTIFIER "(" parameter_list ")" statement_list ENDSUBROUTINE')
    def subroutine_declaration(self, p):
        return {
            "type": "subroutine",
            "name": p.IDENTIFIER,
            "params": p.parameter_list,
            "body": p.statement_list
        }

    @_('SUBROUTINE IDENTIFIER "(" ")" statement_list ENDSUBROUTINE')
    def subroutine_declaration(self, p):
        return {
            "type": "subroutine",
            "name": p.IDENTIFIER,
            "params": [],
            "body": p.statement_list
        }
    
    @_('IDENTIFIER "[" expression_list "]"')
    def list_call(self, p):
        return {
            "type": "list_call",
            "name": p.IDENTIFIER,
            "args": p.expression_list
        }

    @_('IDENTIFIER "(" expression_list ")"')
    def subroutine_call(self, p):
        return {
            "type": "call",
            "name": p.IDENTIFIER,
            "args": p.expression_list
        }

    @_('IDENTIFIER "(" ")"')
    def subroutine_call(self, p):
        return {
            "type": "call",
            "name": p.IDENTIFIER,
            "args": []
        }

    @_('IDENTIFIER')
    def parameter(self, p):
        return p.IDENTIFIER

    @_('parameter_list "," IDENTIFIER')
    def parameter_list(self, p):
        return p.parameter_list + [p.IDENTIFIER]

    @_('IDENTIFIER')
    def parameter_list(self, p):
        return [p.IDENTIFIER]

    @_('IDENTIFIER ":" data_type')
    def field(self, p):
        return {
            "name": p.IDENTIFIER,
            "type": p.data_type
        }

    @_('field_list field')
    def field_list(self, p):
        return p.field_list + [p.field]

    @_('field')
    def field_list(self, p):
        return [p.field]

    @_('CONSTANT IDENTIFIER ASSIGN expression')
    def constant_declaration(self, p):
        return {
            "type": "constant",
            "name": p.IDENTIFIER,
            "value": p.expression
        }

    @_('INT', 'REAL', 'STRING', 'CHAR')
    def data_type(self, p):
        return p[0]

    @_('expression')
    def expression_list(self, p):
        return [p.expression]

    @_('expression "," expression_list')
    def expression_list(self, p):
        return [p.expression] + p.expression_list

    @_('INT')
    def expression(self, p):
        return {
            "type": "literal",
            "value": int(p.INT)
        }

    @_('REAL')
    def expression(self, p):
        return {
            "type": "literal",
            "value": float(p.REAL)
        }

    @_('STRING', 'CHAR')
    def expression(self, p):
        return {
            "type": "literal",
            "value": p[0][1:-1]  # Remove the surrounding quotes
        }

    @_('TRUE', 'FALSE')
    def expression(self, p):
        return {
            "type": "literal",
            "value": True if p[0] == 'TRUE' else False
        }

    @_('IDENTIFIER')
    def expression(self, p):
        return {
            "type": "var",
            "name": p.IDENTIFIER
        }

    @_('expression "+" expression',
       'expression "-" expression',
       'expression "*" expression',
       'expression "/" expression',
       'expression MOD expression',
       'expression DIV expression',
       'expression "<" expression',
       'expression ">" expression',
       'expression "≤" expression',
       'expression "≥" expression',
       'expression "≠" expression',
       'expression "=" expression')
    def expression(self, p):
        return {
            "type": "binop",
            "operator": p[1],
            "left": p.expression0,
            "right": p.expression1
        }

    @_('"(" expression ")"')
    def expression(self, p):
        return p.expression

    @_('NOT expression')
    def expression(self, p):
        return {
            "type": "not",
            "value": p.expression
        }

    @_('expression AND expression')
    def expression(self, p):
        return {
            "type": "and",
            "left": p.expression0,
            "right": p.expression1
        }

    @_('expression OR expression')
    def expression(self, p):
        return {
            "type": "or",
            "left": p.expression0,
            "right": p.expression1
        }

    @_('LEN "(" expression ")"')
    def expression(self, p):
        return {
            "type": "len",
            "value": p.expression
        }

    @_('POSITION "(" expression "," expression ")"')
    def expression(self, p):
        return {
            "type": "position",
            "string": p.expression0,
            "substring": p.expression1
        }

    @_('RANDOM_INT "(" expression "," expression ")"')
    def expression(self, p):
        return {
            "type": "random_int",
            "min": p.expression0,
            "max": p.expression1
        }

    @_('SUBSTRING "(" expression "," expression "," expression ")"')
    def expression(self, p):
        return {
            "type": "substring",
            "string": p.expression0,
            "start": p.expression1,
            "length": p.expression2
        }

    @_('STRING_TO_INT "(" expression ")"')
    def expression(self, p):
        return {
            "type": "string_to_int",
            "value": p.expression
        }

    @_('STRING_TO_REAL "(" expression ")"')
    def expression(self, p):
        return {
            "type": "string_to_real",
            "value": p.expression
        }

    @_('INT_TO_STRING "(" expression ")"')
    def expression(self, p):
        return {
            "type": "int_to_string",
            "value": p.expression
        }

    @_('REAL_TO_STRING "(" expression ")"')
    def expression(self, p):
        return {
            "type": "real_to_string",
            "value": p.expression
        }

    @_('CHAR_TO_CODE "(" expression ")"')
    def expression(self, p):
        return {
            "type": "char_to_code",
            "value": p.expression
        }

    @_('CODE_TO_CHAR "(" expression ")"')
    def expression(self, p):
        return {
            "type": "code_to_char",
            "value": p.expression
        }
        
    @_('USERINPUT')
    def expression(self, p):
        return {
            "type": "userinput"
        }
    
    @_('subroutine_call')
    def expression(self, p):
        return p.subroutine_call
    
    @_('list_call')
    def expression(self, p):
        return p.list_call

    @_('expression')
    def expression_statement(self, p):
        return {
            "type": "expression",
            "value": p.expression
        }

    def error(self, p):
        if p:
            print(f"Syntax error at line {p.lineno}, token={p.type}")
            self.errok()
        else:
            print("Syntax error at EOF")
