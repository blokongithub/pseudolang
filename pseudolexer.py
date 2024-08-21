from sly import Lexer

class Pseudolexer(Lexer):
    # List of token names
    tokens = { ID, NUMBER, ASSIGN, EQ, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN, IF, ELSE, THEN, ENDIF, RETURN }

    # String containing ignored characters between tokens
    ignore = ' \t'
    ignore_comment = r'\#.*'

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
    LPAREN  = r'\('
    RPAREN  = r'\)'
    
    @_(r'\d+')
    def NUMBER(self, token):
        token.value = int(token.value)
        return token
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)
    def error(self, token):
        print(f"Invalid token: {token.value}")
        self.index += 1
