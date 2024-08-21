from sly import Parser
from pseudolexer import Pseudolexer

class Pseudoparser(Parser):
    tokens = Pseudolexer.tokens

  
    def __init__(self): 
        self.variables = { }
    @_('ID ASSIGN expr')
    def statement(self, p):
        self.variables[p.ID] = p.expr
        return p.expr
    @_('expr')
    def statement(self, p):
        return p.expr
    @_('ID')
    def expr(self, p):
        return self.variables[p.ID]
    @_("expr PLUS term")
    def expr(self, p):
        return p.expr + p.term
    @_("expr MINUS term")
    def expr(self, p):
        return p.expr - p.term
    @_("term")
    def expr(self, p):
        return p.term
    @_("term TIMES factor")
    def term(self, p):
        return p.term * p.factor
    @_("term DIVIDE factor")
    def term(self, p):
        return p.term / p.factor
    @_("factor")
    def term(self, p):
        return p.factor
    @_("NUMBER")
    def factor(self, p):
        return p.NUMBER
    @_("LPAREN expr RPAREN")
    def factor(self, p):
        return p.expr 