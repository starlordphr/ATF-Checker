import ply.yacc as yacc
from atfflex import AtfLexer

from Models.Structure import Structure

class AtfParser(object):
    tokens = AtfLexer.tokens

    def __init__(self, fileName, languageFile, tabmodule='parsetab'):
        self.parser = yacc.yacc(module=self, tabmodule=tabmodule)
        self.objStructure = Structure(fileName)
        self.fileName = fileName
        self.languageFile = languageFile

    def p_atf_text(self, p):
        """atf_text : tablet
                    | bulla
                    | tag
                    | prism
                    | barrel
                    | cylinder
                    | brick
                    | cone
                    | sealing
                    | seal
                    | composite"""
        #self.write_to_file(self.fileName, "-----> ATF Text Detected: "+self.objStructure.pNumber)

    def p_tablet(self, p):
        """tablet : ATF_HEADER TABLET newline surface_structure
                  | ATF_HEADER TABLET newline surface_structure ENVELOPE newline surface_structure"""
        #self.write_to_file(self.fileName, "-----> Complete Tablet Detected")

    def p_bulla(self, p):
        """bulla : ATF_HEADER OBJECT BULLA newline surface_structure"""
        #self.write_to_file(self.fileName, "-----> Complete Bulla Detected")

    def p_tag(self, p):
        """tag : ATF_HEADER OBJECT TAG newline surface_structure"""
        #self.write_to_file(self.fileName, "-----> Complete Tag Detected")

    def p_prism(self, p):
        """prism : ATF_HEADER OBJECT PRISM newline surface_structure"""
        #self.write_to_file(self.fileName, "-----> Complete Prism Detected")

    def p_barrel(self, p):
        """barrel : ATF_HEADER OBJECT BARREL newline surface_structure"""
        #self.write_to_file(self.fileName, "-----> Complete Barrel Detected")

    def p_cylinder(self, p):
        """cylinder : ATF_HEADER OBJECT CYLINDER newline surface_structure"""
        #self.write_to_file(self.fileName, "-----> Complete Cylinder Detected")

    def p_brick(self, p):
        """brick : ATF_HEADER OBJECT BRICK newline surface_structure"""
        #self.write_to_file(self.fileName, "-----> Complete Brick Detected")

    def p_cone(self, p):
        """cone : ATF_HEADER OBJECT CONE newline surface_structure"""
        #self.write_to_file(self.fileName, "-----> Complete Cone Detected")

    def p_sealing(self, p):
        """sealing : ATF_HEADER OBJECT SEALING newline surface_structure"""
        #self.write_to_file(self.fileName, "-----> Complete Sealing Detected")

    def p_seal(self, p):
        """seal : ATF_HEADER OBJECT SEAL newline surface_structure"""
        #self.write_to_file(self.fileName, "-----> Complete Seal Detected")

    def p_composite(self, p):
        """composite : ATF_HEADER OBJECT COMPOSITE newline surface_structure"""
        #self.write_to_file(self.fileName, "-----> Complete Composite Detected")

    def p_ATF_HEADER(self, p):
        """ATF_HEADER : designation
                      | ATF_HEADER language_comment
                      | ATF_HEADER lexical_comment
                      | ATF_HEADER link_comment
                      | ATF_HEADER CBS_comment
                      | ATF_HEADER version_comment"""
        #self.write_to_file(self.fileName, "-----> ATF Header")

    def p_designation(self, p):
        """designation : PNUMBER EQUALS string newline"""
        self.objStructure.pNumber = p[1]
        #self.write_to_file(self.fileName, "-----> Designation Line")

    def p_language_comment(self, p):
        """language_comment : ATF LANG string newline"""
        #self.write_to_file(self.fileName, "-----> Language Line")

    def p_lexical_comment(self, p):
        """lexical_comment : ATF USE LEXICAL newline"""
        #self.write_to_file(self.fileName, "-----> Lexical Line")


    def p_link_comment(self, p):
        """link_comment : LINK DEF string EQUALS QNUMBER EQUALS string newline
                        | LINK DEF string EQUALS QNUMBER newline"""
        #self.write_to_file(self.fileName, "-----> Link Line")

    def p_CBS_comment(self, p):
        """CBS_comment : CBS string newline"""
        #self.write_to_file(self.fileName, "-----> CBS Line")

    def p_version_comment(self, p):
        """version_comment : VERSION VNUMBER newline"""
        #self.write_to_file(self.fileName, "-----> Version Line")

    def p_surface_structure(self, p):
        """surface_structure : surface_text
                            | FRAGMENT newline paragraph
                            | FRAGMENT newline surface_text
                            | surface_structure surface_text
                            | surface_structure FRAGMENT newline paragraph
                            | surface_structure FRAGMENT newline surface_text"""

        #self.write_to_file(self.fileName, "-----> Surface Structure Detected")

    def p_surface_text(self, p):
        """surface_text : column_text
                        | SURFACE_TYPE newline column_text
                        | SURFACE_TYPE newline paragraph
                        | SURFACE_TYPE newline SEGMENT newline column_text
                        | SURFACE_TYPE newline SEGMENT newline paragraph
                        | surface_text column_text
                        | surface_text SURFACE_TYPE newline column_text
                        | surface_text SURFACE_TYPE newline paragraph
                        | surface_text SEGMENT newline column_text
                        | surface_text SEGMENT newline paragraph"""

        '''if len(p) == 4:
            if "seal" in str(p[1]):
                self.objStructure.SetSealStatus()
            else:
                if self.objStructure.CheckSealStatus():
                    self.write_to_file(self.fileName, "xxxxxxx> General Warning: Seal is not in the end of ATF")

        elif len(p) == 5:
            if "seal" in str(p[2]):
                self.objStructure.SetSealStatus()
            else:
                if self.objStructure.CheckSealStatus():
                    self.write_to_file(self.fileName, "xxxxxxx> General Warning: Seal is not in the end of ATF")'''

        #self.write_to_file(self.fileName, "-----> Surface Text Detected")

    def p_column_text(self, p):
        """column_text : column
                | column_text column"""
            #    | column_text newline""" #text seal

        #self.write_to_file(self.fileName, "-----> Multiple Column Detected")

    def p_column(self, p):
        """column : COLUMN newline paragraph"""
        #self.write_to_file(self.fileName, "-----> Column Detected")

    def p_paragraph(self, p):
        """paragraph : text_line
                     | comment
                     | paragraph text_line
                     | paragraph comment"""
        '''if(len(p) == 2):
            self.write_to_file(self.fileName, "-----> Paragraph: "+str(p[1]))
        elif(len(p) == 3):
            self.write_to_file(self.fileName, "-----> Paragraph: "+str(p[1])+" "+str(p[2]))'''

    def p_comment(self, p):
        """comment : DOLLAR string newline
                   | HASH string newline
                   | LEGACY_COMMENT string newline"""
        #self.write_to_file(self.fileName, "-----> Comment Found")

    def p_text_line(self, p):
        """text_line : LINE string newline""" #Cannot detect last line of text in paragraph maybe adding rule for pnumber will fix that
        #self.write_to_file(self.fileName, "-----> Text Line : "+str(p[1])+" "+str(p[2]))

    def p_newline(self, p):
        "newline : NEWLINE"
        #self.write_to_file(self.fileName, "newline")

    def p_keywords(self, p):
        """keywords : EQUALS
                    | AMPERSAND
                    | COLON
                    | QNUMBER
                    | ATF
                    | LANG
                    | USE
                    | LEXICAL
                    | LINK
                    | DEF
                    | CBS
                    | DOLLAR
                    | LEGACY_COMMENT
                    | VERSION
                    | OBJECT
                    | TABLET
                    | BULLA
                    | TAG
                    | PRISM
                    | BARREL
                    | CYLINDER
                    | BRICK
                    | CONE
                    | SEALING
                    | ENVELOPE
                    | LINE
                    | COLUMN
                    | FRAGMENT
                    | SURFACE_TYPE"""
        #self.write_to_file(self.fileName, "-----> Keyword Found")

    def p_string(self, p):
        """string : STRING
                  | keywords
                  | string STRING
                  | string keywords"""
        '''if(len(p) == 2):
            self.write_to_file(self.fileName, "String: "+str(p[1]))
        elif(len(p) == 3):
            self.write_to_file(self.fileName, "String: "+str(p[1])+" "+str(p[2]))'''

    def p_error(self, p):
        #self.write_to_file(self.fileName, "-----> CDLI could not parse token "+str(p.value))
        if not p is None:
            self.write_to_file(self.fileName, "-----> CDLI could not parse token: %s, Line No: %s, Position: %s" %(p.value, p.lineno, p.lexpos))
        #valuestring = p.value
        #self.write_to_file(self.fileName, "Syntax Error: "+str(p.lineno)+" "+str(p.lexpos)+" "+str(valuestring))
        # All errors currently unrecoverable
        # So just throw
        # Add list of params so PyORACC users can build their own error msgs.

    def write_to_file(self, file, content):
        text_file = open("/atfchecker_data/output/"+file, "a")
        text_file.write(content+"\n")
        text_file.close()
