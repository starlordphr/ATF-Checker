import ply.yacc as yacc
from atfflex import AtfLexer

class AtfParser(object):
    tokens = AtfLexer.tokens

    def __init__(self, tabmodule='parsetab'):
        self.parser = yacc.yacc(module=self, tabmodule=tabmodule)

    '''def p_catf_text(self, p):
        """catf_text : designation language_comment"""
        self.write_to_file("atf Detected\n")'''

    '''def p_designation(self, p):
        """designation : PNUMBER EQUALS string newline"""
        self.write_to_file("Designation Line : "+str(p[1])+" "+str(p[2])+" "+str(p[3])+" "+str(p[4]))'''

    '''def p_language_comment(self, p):
        """language_comment : ATF LANG string newline"""
        self.write_to_file("Language Line : "+str(p[1])+" "+str(p[2])+" "+str(p[3])+" "+str(p[4]))'''

    '''def p_lexical_comment(self, p):
        """lexical_comment : ATF USE LEXICAL newline"""
        self.write_to_file("Lexical Line : "+str(p[1])+" "+str(p[2])+" "+str(p[3])+" "+str(p[4]))'''

    def p_link_comment(self, p):
        """link_comment : LINK DEF string EQUALS QNUMBER EQUALS string newline
                        | LINK DEF string EQUALS QNUMBER newline"""
        if(len(p) == 9):
            self.write_to_file("Link Line : "+str(p[1])+" "+str(p[2])+" "+str(p[3])+" "+str(p[4])+" "+str(p[5])+" "+str(p[6])+" "+str(p[7]))
        elif(len(p) == 7):
            self.write_to_file("Link Line : "+str(p[1])+" "+str(p[2])+" "+str(p[3])+" "+str(p[4])+" "+str(p[5]))

    '''def p_CBS_comment(self, p):
        """CBS_comment : CBS string newline"""
        self.write_to_file("CBS Line : "+str(p[1])+" "+str(p[2]))'''

    '''def p_version_comment(self, p):
        """version_comment : VERSION VNUMBER newline"""
        self.write_to_file("Version Line : "+str(p[1])+" "+str(p[2]))'''

    def p_string(self, p):
        """string : STRING
                  | string STRING
                  | string EQUALS"""
        if(len(p) == 2):
            print("String Line 1: "+str(p[1]))
        elif(len(p) == 3):
            print("String Line 2: "+str(p[1])+" "+str(p[2]))

    def p_newline(self, p):
        "newline : NEWLINE"
        print "newline"

    def p_error(self, p):
        formatstring = u"CDLI could not parse token '{}'.".format(p)
        valuestring = p.value
        #raise SyntaxError(formatstring,(None, p.lineno, p.lexpos, valuestring))
        # All errors currently unrecoverable
        # So just throw
        # Add list of params so PyORACC users can build their own error msgs.

    def write_to_file(self, content):
        text_file = open("Output.txt", "a")
        text_file.write(content+"\n")
        text_file.close()

'''lexical_comment : HASH ATF COLON USE LEXICAL newline
                    | HASH ATF USE LEXICAL newline
                    | ATF COLON USE LEXICAL newline
                    | ATF USE LEXICAL newline'''
