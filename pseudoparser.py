from sly import Parser
from pseudolexer import Pseudolexer

class Pseudoparser(Parser):
    tokens = Pseudolexer.tokens

  
    def __init__(self): 
        self.variables = { } 