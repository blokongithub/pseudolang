# type: ignore

from sly import Lexer

class PseudoCodeLexer(Lexer):
    tokens = { IDENTIFIER, CONSTANT, INT, REAL, STRING, CHAR, 
               AND, OR, NOT, IF, THEN, ELSE, ENDIF, WHILE, ENDWHILE,
               REPEAT, UNTIL, FOR, TO, STEP, ENDFOR, IN, RECORD, ENDRECORD,
               TRUE, FALSE, OUTPUT, USERINPUT, RANDOM_INT, LEN, POSITION,
               SUBSTRING, STRING_TO_INT, STRING_TO_REAL, INT_TO_STRING,
               REAL_TO_STRING, CHAR_TO_CODE, CODE_TO_CHAR, MOD, DIV, DO, ASSIGN,
               SUBROUTINE, ENDSUBROUTINE, RETURN, BREAK, ISINTEGER }

    literals = {'=', '+', '-', '*', '/', '(', ')', '[', ']', ',', '<', '>', '≤', '≥', '≠'}
    
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
    
    STRING = r'\'[^\']*\''
    CHAR = r'\'[^\']\''

    REAL = r'\d+\.\d+'
    INT = r'\d+'
    
    IDENTIFIER['RETURN'] = RETURN
    IDENTIFIER['BREAK'] = BREAK
    IDENTIFIER['CONSTANT'] = CONSTANT
    IDENTIFIER['AND'] = AND
    IDENTIFIER['DO'] = DO
    IDENTIFIER['OR'] = OR
    IDENTIFIER['NOT'] = NOT
    IDENTIFIER['IF'] = IF
    IDENTIFIER['THEN'] = THEN
    IDENTIFIER['ELSE'] = ELSE
    IDENTIFIER['ENDIF'] = ENDIF
    IDENTIFIER['WHILE'] = WHILE
    IDENTIFIER['ENDWHILE'] = ENDWHILE
    IDENTIFIER['REPEAT'] = REPEAT
    IDENTIFIER['UNTIL'] = UNTIL
    IDENTIFIER['FOR'] = FOR
    IDENTIFIER['TO'] = TO
    IDENTIFIER['STEP'] = STEP
    IDENTIFIER['ENDFOR'] = ENDFOR
    IDENTIFIER['IN'] = IN
    IDENTIFIER['RECORD'] = RECORD #TODO (records have not been added to the parser or interpreter)
    IDENTIFIER['ENDRECORD'] = ENDRECORD #TODO (records have not been added to the parser or interpreter)
    IDENTIFIER['TRUE'] = TRUE
    IDENTIFIER['FALSE'] = FALSE
    IDENTIFIER['OUTPUT'] = OUTPUT
    IDENTIFIER['USERINPUT'] = USERINPUT
    IDENTIFIER['RANDOM_INT'] = RANDOM_INT
    IDENTIFIER['LEN'] = LEN
    IDENTIFIER['POSITION'] = POSITION
    IDENTIFIER['SUBSTRING'] = SUBSTRING
    IDENTIFIER['STRING_TO_INT'] = STRING_TO_INT
    IDENTIFIER['STRING_TO_REAL'] = STRING_TO_REAL
    IDENTIFIER['INT_TO_STRING'] = INT_TO_STRING
    IDENTIFIER['REAL_TO_STRING'] = REAL_TO_STRING
    IDENTIFIER['CHAR_TO_CODE'] = CHAR_TO_CODE
    IDENTIFIER['CODE_TO_CHAR'] = CODE_TO_CHAR
    IDENTIFIER['MOD'] = MOD
    IDENTIFIER['DIV'] = DIV
    IDENTIFIER['SUBROUTINE'] = SUBROUTINE
    IDENTIFIER['ENDSUBROUTINE'] = ENDSUBROUTINE
    IDENTIFIER['ISINTEGER'] = ISINTEGER
    
    ASSIGN = r'<-'
    
    ignore = ' \t'
    
    ignore_newline = r'\n+'

    def error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        self.index += 1
