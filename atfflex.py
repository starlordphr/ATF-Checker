import ply.lex as lex
import re
import sys

from SupportFiles.Pnumber import Pnumber
from SupportFiles.Qnumber import Qnumber

class AtfLexer(object):

    def __init__(self, skipinvalid=False, debug=0):
        self.lexer = lex.lex(module=self, reflags=re.MULTILINE, debug=debug)
        self.pnumberObj = Pnumber()
        self.qnumberObj = Qnumber()

    #List of token names
    base_tokens = ['EQUALS',
                   'NEWLINE',
                   'AMPERSAND',
                   'HASH',
                   'DOLLAR',
                   'COLON',
                   'QNUMBER']

    comment_tokens = ['ATF',
                      'LANG',
                      'USE',
                      'LEXICAL',
                      'LINK',
                      'DEF',
                      'CBS',
                      'VERSION',
                      'VNUMBER']

    designation_tokens = ['PNUMBER']

    general_tokens = ['STRING']

    tokens = sorted(list(set(
        base_tokens +
        comment_tokens +
        designation_tokens +
        general_tokens)))

    #Regular expression rules for simple tokens

    #Regular expression rule with some action code
    def t_PNUMBER(self, t):
        r'&P[0-9]{6}'
        value,status = self.pnumberObj.CheckPMap(t.value[1:])
        t.value = t.value.replace(t.value,value)

        if not status:
            self.write_to_file("Incorrect Pnumber : "+str(t.value))
            t.lexer.skip(1)
            return

        print "Pnumber:"+t.value
        return t

    def t_QNUMBER(self, t):
        r'Q[0-9]{6}'
        print "Qnumber:"+t.value
        if(not self.qnumberObj.CheckQnumber(t.value)):
            self.write_to_file("Warning: Qnumber not recognised.")
        return t

    def t_VNUMBER(self, t):
        r'0\.[1-9]{1}'
        print "Vnumber:"+t.value
        return t

    # In the base state, a newline doesn't change state
    def t_NEWLINE(self, t):
        r'\s*[\n\r]'
        return t

    def t_ATF(self, t):
        r'#atf:'
        print "Atf:"+t.value
        return t

    def t_LINK(self, t):
        r'#link:'
        print "Link:"+t.value
        return t

    def t_LANG(self, t):
        r'lang'
        print "Lang:"+t.value
        return t

    def t_LEXICAL(self, t):
        r'lexical'
        print "Lexical:"+t.value
        return t

    def t_USE(self, t):
        r'use'
        print "Use:"+t.value
        return t

    def t_DEF(self, t):
        r'def'
        print "Def:"+t.value
        return t

    def t_CBS(self, t):
        r'#CBS'
        print "CBS:"+t.value
        return t

    def t_VERSION(self, t):
        r'#version:'
        print "Version:"+t.value
        return t

    def t_EQUALS(self, t):
        r'\='
        print "Equals:"+t.value
        #t.lexer.push_state('flagged')
        return t

    def t_COLON(self, t):
        r'\:'
        return t

    t_AMPERSAND = "\&"
    t_HASH = "\#"
    t_DOLLAR = "\$"

    def t_STRING(self, t):
        #r"[A-Za-z0-9\(\)\,\-\+\[\]\;\=\/\?\:\']+"
        r"[^\s]+"
        print "String:"+t.value
        #t.lexer.push_state('string')
        #print t.value
        return t

    # Error handling rule
    def t_error(self, t):
        #print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def write_to_file(self, content):
        text_file = open("Output.txt", "a")
        text_file.write(content+"\n")
        text_file.close()
