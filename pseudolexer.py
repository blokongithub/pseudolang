from sly import Lexer

class Pseudolexer(Lexer):
    # List of token names
    tokens = { ID, NUMBER, ASSIGN, EQ, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN, IF, ELSE, THEN, ENDIF, RETURN }
    literals = { '(', ')', '{', '}', '[', ']' ';' }

    # String containing ignored characters between tokens
    ignore = ' \t'

    # Regular expression rules for tokens
    ID      = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['IF']        = IF
    ID['ELSE']      = ELSE
    ID['THEN']      = THEN
    ID['ENDIF']     = ENDIF
    ID['RETURN']    = RETURN
    
    NUMBER  = r'\d+'
    ASSIGN  = r'<-'
    EQ      = r'='
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    
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
    
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')
        
    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1
