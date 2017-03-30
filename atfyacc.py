import ply.yacc as yacc
from atfflex import AtfLexer

class AtfParser(object):
    tokens = AtfLexer.tokens
    text = ""

    def __init__(self, tabmodule='parsetab'):
        self.parser = yacc.yacc(module=self, tabmodule=tabmodule)

    def p_description(self, p):
        "description : PNUMBER EQUALS string newline"
        print("Description Line : ",p[1],p[2],p[3],p[4])

    def p_string(self, p):
        """string : NORMALSTRING
                  | string NORMALSTRING"""
        if(len(p) == 2):
            print("String Line 1: ",p[1])
        elif(len(p) == 3):
            print("String Line 2: ",p[1],p[2])

    def p_newline(self, p):
        "newline : NEWLINE"

    def p_error(self, p):
        formatstring = u"CDLI could not parse token '{}'.".format(p)
        valuestring = p.value
        #raise SyntaxError(formatstring,(None, p.lineno, p.lexpos, valuestring))
        # All errors currently unrecoverable
        # So just throw
        # Add list of params so PyORACC users can build their own error msgs.
