import ply.lex as lex
import re
import sys

from SupportFiles.Pnumber import Pnumber

class AtfLexer(object):

    def __init__(self, skipinvalid=False, debug=0):
        self.lexer = lex.lex(module=self, reflags=re.MULTILINE, debug=debug)
        self.pnumberObj = Pnumber()

    #List of token names
    tokens = ['PNUMBER',
              'EQUALS',
              'NEWLINE',
              'NORMALSTRING']

    #Regular expression rules for simple tokens

    #Regular expression rule with some action code
    def t_PNUMBER(self, t):
        r'&P[0-9]{6}'
        value,status = self.pnumberObj.CheckPMap(t.value[1:])
        t.value = t.value.replace(t.value,value)

        if not status:
            print "Incorrect Pnumber : "+t.value
            t.lexer.skip(1)
            return
        return t

    def t_EQUALS(self, t):
        "\="
        #t.lexer.push_state('flagged')
        return t

    # In the base state, a newline doesn't change state
    def t_NEWLINE(self, t):
        r'\s*[\n\r]'
        return t

    def t_NORMALSTRING(self, t):
        r"[A-Za-z0-9\,\/\-\'\.]+"
        #t.lexer.push_state('string')
        return t

    # Error handling rule
    def t_error(self, t):
        #print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)
