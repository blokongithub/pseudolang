from sly import Lexer

class Pseudolexer(Lexer):
    tokens = { 
            ID, 
            NUMBER,
            FLOAT, 
            STRING,
            ASSIGN,
            EQ, 
            PLUS, 
            MINUS, 
            TIMES,
            DIVIDE, 
            LPAREN, 
            RPAREN, 
            IF, 
            ELSE, 
            THEN, 
            ENDIF,
            RETURN,
            LT,
            LE,
            GT,
            GE,
            NE,
            WHILE,
            ENDWHILE,
            FOR,
            ENDFOR,
            IN,
            CONSTANT,
            REPEAT,
            UNTIL,
            STEP,
            ELSEIF,
            MODULO,
            DIV,
            OUTPUT,
            RECORD,
            ENDRECORD,
            SUBROUTINE,
            ENDSUBROUTINE,
            LEN,
            POSITION,
            SUBSTRING,
            STRING_TO_INT,
            STRING_TO_REAL,
            INT_TO_STRING,
            REAL_TO_STRING,
            CHAR_TO_CODE,
            CODE_TO_CHAR,
            USERINPUT,
            RANDOM_INT,
            LPAREN,
            RPAREN,       
            }
    literals = {'{', '}', '[', ']' ';' }

    # string containing ignored characters between tokens
    ignore = ' \t'

    # regular expression rules for tokens
    ID                      = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['ELSE IF']           = ELSEIF
    ID['IF']                = IF
    ID['ELSE']              = ELSE
    ID['THEN']              = THEN
    ID['ENDIF']             = ENDIF
    ID['RETURN']            = RETURN
    ID['WHILE']             = WHILE
    ID['ENDWHILE']          = ENDWHILE
    ID['FOR']               = FOR
    ID['ENDFOR']            = ENDFOR
    ID['IN']                = IN
    ID['CONSTANT']         = CONSTANT
    ID['REPEAT']            = REPEAT
    ID['UNTIL']             = UNTIL
    ID['STEP']              = STEP
    ID['MOD']               = MODULO
    ID['DIV']               = DIV
    ID['OUTPUT']            = OUTPUT
    ID['RECORD']            = RECORD
    ID['ENDRECORD']         = ENDRECORD
    ID['SUBROUTINE']        = SUBROUTINE
    ID['ENDSUBROUTINE']     = ENDSUBROUTINE
    ID['LEN']               = LEN
    ID['POSITION']          = POSITION
    ID['SUBSTRING']         = SUBSTRING
    ID['STRING_TO_INT']     = STRING_TO_INT
    ID['STRING_TO_REAL']    = STRING_TO_REAL
    ID['INT_TO_STRING']     = INT_TO_STRING
    ID['REAL_TO_STRING']    = REAL_TO_STRING
    ID['CHAR_TO_CODE']      = CHAR_TO_CODE
    ID['CODE_TO_CHAR']      = CODE_TO_CHAR
    ID['USERINPUT']         = USERINPUT
    ID['RANDOM_INT']        = RANDOM_INT
    
    FLOAT   = r'\d+\.\d+'
    NUMBER  = r'\d+'
    STRING  = r'\".*?\"'
    ASSIGN  = r'<-'
    EQ      = r'='
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    LE      = r'<='
    LT      = r'<'
    GE      = r'>='
    GT      = r'>'
    NE      = r'!='
    RPAREN  = r'\)'
    LPAREN  = r'\('
    
    ignore_comment = r'\#.*'
    
    def find_column(text, token):
        last_cr = text.rfind('\n', 0, token.index)
        if last_cr < 0:
            last_cr = 0
        column = (token.index - last_cr) + 1
        return column
    
    @_(r'\d+')
    def NUMBER(self, token):
        token.value = int(token.value)
        return token
    @_(r'\d+\.\d+')
    def FLOAT(self, token):
        token.value = float(token.value)
        return token
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')
        
    def error(self, t):
        print('line %d: bad character %r' % (self.lineno, t.value[0]))
        self.index += 1
