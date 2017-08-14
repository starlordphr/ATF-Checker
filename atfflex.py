import ply.lex as lex
import re
import sys
import os

from SupportFiles.Pnumber import Pnumber
from SupportFiles.Qnumber import Qnumber
from Models.Structure import Structure

counter = 0

class AtfLexer(object):

    def __init__(self, fileName, languageFile, skipinvalid=False, debug=0):
        self.lexer = lex.lex(module=self, reflags=re.MULTILINE, debug=debug)
        self.pnumberObj = Pnumber(fileName)
        self.qnumberObj = Qnumber()
        self.objStructure = Structure(fileName)
        self.fileName = fileName
        self.pNumber = ""
        self.errors = ""
        self.databaseDirectoryPath = "/Volumes/cdli_www_2/transfers/cdlicore/atfchecker_helper"
        self.languageFile = languageFile
        self.tokenList = list()
        self.signList = list()
        self.testTokenList = list()
        self.testSignList = list()
        self.LoadLanguageToMemory()
        self.errorText = ""
        self.line = False


    #List of token names
    base_tokens = ['EQUALS',
                   'NEWLINE',
                   'AMPERSAND',
                   'HASH',
                   'COLON',
                   'QNUMBER']

    comment_tokens = ['ATF',
                      'LANG',
                      'USE',
                      'LEXICAL',
                      'LINK',
                      'DEF',
                      'CBS',
                      'DOLLAR',
                      'LEGACY_COMMENT',
                      'VERSION',
                      'VNUMBER']

    structure_tokens = ['OBJECT',
                        'TABLET',
                        'BULLA',
                        'TAG',
                        'PRISM',
                        'BARREL',
                        'CYLINDER',
                        'BRICK',
                        'CONE',
                        'SEALING',
                        'SEAL',
                        'COMPOSITE',
                        'ENVELOPE',
                        'LINE',
                        'COLUMN',
                        'FRAGMENT',
                        'SURFACE_TYPE',
                        'SEGMENT']

    designation_tokens = ['PNUMBER']

    general_tokens = ['STRING']

    tokens = sorted(list(set(
        base_tokens +
        comment_tokens +
        designation_tokens +
        structure_tokens +
        general_tokens)))

    #Regular expression rules for simple tokens

    #Regular expression rule with some action code
    def t_PNUMBER(self, t):
        r'&P[0-9]{6}'
        value,status,errorValue = self.pnumberObj.CheckPMap(t.value[1:])
        if errorValue:
            self.errors += errorValue+"\n"
        #t.value = t.value.replace(t.value,value)
        self.objStructure.surfaceList[:] = []

        if not status:
            self.errors += "\nxxxxxxx> Incorrect Pnumber : "+str(t.value)+"\n"
            t.lexer.skip(1)
            return

        #self.write_to_file(self.fileName, "\n\n-----> Pnumber:"+t.value)
        self.objStructure.ResetObjectType()
        self.objStructure.ResetColumnCounter()
        self.pNumber = t.value[1:]
        return t

    def t_QNUMBER(self, t):
        r'Q[0-9]{6}'
        self.write_to_file(self.fileName, "Qnumber:"+t.value)
        if(not self.qnumberObj.CheckQnumber(t.value)):
            self.errors += "Warning: Qnumber not recognised.\n"
        return t

    def t_VNUMBER(self, t):
        r'0\.[0-9]{1}'
        #self.write_to_file(self.fileName, "Vnumber:"+t.value)
        return t

    def t_LINE(self, t):
        r"[0-9]+[\']?\."
        t.lexer.lineno += len(t.value)
        self.line = True
        #self.write_to_file(self.fileName, "Flex Line: "+t.value)
        return t

    # In the base state, a newline doesn't change state
    def t_NEWLINE(self, t):
        r'\s*[\n\r]'
        self.line = False
        #self.write_to_file(self.fileName, "Flex Newline")
        return t

    def t_ATF(self, t):
        r'#atf:'
        #self.write_to_file(self.fileName, "Atf:"+t.value)
        return t

    def t_LINK(self, t):
        r'#link:'
        #self.write_to_file(self.fileName, "Link:"+t.value)
        return t

    def t_LANG(self, t):
        r'lang'
        #self.write_to_file(self.fileName, "Lang:"+t.value)
        return t

    def t_LEXICAL(self, t):
        r'lexical'
        #self.write_to_file(self.fileName, "Lexical:"+t.value)
        return t

    def t_USE(self, t):
        r'use'
        #self.write_to_file(self.fileName, "Use:"+t.value)
        return t

    def t_DEF(self, t):
        r'def'
        #self.write_to_file(self.fileName, "Def:"+t.value)
        return t

    def t_CBS(self, t):
        r'#CBS'
        #self.write_to_file(self.fileName, "CBS:"+t.value)
        return t

    def t_VERSION(self, t):
        r'#version:'
        #self.write_to_file(self.fileName, "Version:"+t.value)
        return t

    def t_OBJECT(self, t):
        r'@object'
        #self.write_to_file(self.fileName, "Object:"+t.value)
        return t

    def t_TABLET(self, t):
        r'@tablet'
        #self.write_to_file(self.fileName, "Tablet:"+t.value)
        #self.objStructure.SetObjectType(str(t.value))
        return t

    def t_BULLA(self, t):
        r'bulla[\s]?$'
        #self.write_to_file(self.fileName, "Bulla:"+t.value)
        self.objStructure.SetObjectType(str(t.value))
        return t

    def t_TAG(self, t):
        r'tag[\s]?$'
        #self.write_to_file(self.fileName, "Tag:"+t.value)
        return t

    def t_PRISM(self, t):
        r'prism[\s]?$'
        #self.write_to_file(self.fileName, "Prism:"+t.value)
        self.objStructure.SetObjectType(str(t.value))
        return t

    def t_BARREL(self, t):
        r'barrel[\s]?$'
        #self.write_to_file(self.fileName, "Barrel:"+t.value)
        self.objStructure.SetObjectType(str(t.value))
        return t

    def t_CYLINDER(self, t):
        r'cylinder[\s]?$'
        #self.write_to_file(self.fileName, "Cylinder:"+t.value)
        self.objStructure.SetObjectType(str(t.value))
        return t

    def t_BRICK(self, t):
        r'brick[\s]?$'
        #self.write_to_file(self.fileName, "Brick:"+t.value)
        self.objStructure.SetObjectType(str(t.value))
        return t

    def t_CONE(self, t):
        r'cone(\sfragment)?[\s]?$'
        #self.write_to_file(self.fileName, "Cone:"+t.value)
        self.objStructure.SetObjectType(str(t.value))
        return t

    def t_SEALING(self, t):
        r'sealing[\s]?$'
        #self.write_to_file(self.fileName, "Sealing:"+t.value)
        self.objStructure.SetObjectType(str(t.value))
        return t

    def t_SEAL(self, t):
        r'seal$'
        #self.write_to_file(self.fileName, "Seal:"+t.value)
        self.objStructure.SetObjectType(str(t.value))
        return t

    def t_COMPOSITE(self, t):
        r'composite\stext'
        #self.write_to_file(self.fileName, "Composite:"+t.value)
        self.objStructure.SetObjectType(str(t.value))
        return t

    def t_ENVELOPE(self, t):
        r'@envelope'
        self.objStructure.SetSurface(str(t.value))
        #self.write_to_file(self.fileName, "Envelope:"+t.value)
        return t

    def t_FRAGMENT(self, t):
        r'@fragment\s[a-zA-Z0-9]+[\']?'
        self.objStructure.SetSurface(str(t.value))
        #self.write_to_file(self.fileName, "Fragment Type:"+t.value+"\tList: "+str(self.objStructure.surfaceList))
        return t

    def t_SURFACE_TYPE(self, t):
        r'@(obverse[\?]?|reverse[\?]?|top[\?]?|bottom[\?]?|left[\?]?|right[\?]?|seal\s([A-Z]{1}|[0-9]+)?|surface [a-zA-Z0-9]+|face [a-zA-Z0-9]+)'
        self.objStructure.SetSurface(str(t.value))
        #self.objStructure.CheckSurfaceRules()
        #self.write_to_file(self.fileName, "Surface Type:"+t.value+"\tList: "+str(self.objStructure.surfaceList))
        return t

    def t_SEGMENT(self, t):
        r'@m=segment\s[a-zA-Z0-9]+|@canto\s[a-zA-Z0-9]+'
        self.objStructure.SetSurface(str(t.value))
        #self.write_to_file(self.fileName, "Surface Segment Type:"+t.value+"\tList: "+str(self.objStructure.surfaceList))
        return t

    def t_COLUMN(self, t):
        r'@column\s[0-9]+[\'\?]?'
        #self.write_to_file(self.fileName, 'Flex Column: '+t.value)
        self.objStructure.IncrementColumnCounter()
        return t

    def t_EQUALS(self, t):
        r'\='
        #self.write_to_file(self.fileName, "Equals:"+t.value)
        #t.lexer.push_state('flagged')
        return t

    def t_COLON(self, t):
        r'\:'
        return t

    t_AMPERSAND = "\&"

    def t_HASH(self, t):
        r"\#"
        #self.write_to_file(self.fileName, "HASH: "+t.value)
        return t

    def t_LEGACY_COMMENT(self, t):
        r">>(Q[0-9]{6}|[A-Z]{1})"
        #self.write_to_file(self.fileName, "Legacy Comment: "+t.value)
        return t

    def t_DOLLAR(self, t):
        r"\$"
        #self.write_to_file(self.fileName, "DOLLAR: "+t.value)
        return t

    def t_STRING(self, t):
        #r"[A-Za-z0-9\(\)\,\-\+\[\]\;\=\/\?\:\']+"
        r"[^\s]+"
        #print "String:"+t.value
        #t.lexer.push_state('string')
        #self.write_to_file(self.fileName, "Flex String: "+t.value)
        p = re.compile("[0-9]+\'?. (.*)")
        stringValue = t.value

        if self.line == True:
            if "$)" in t.value and "($" in t.value:
                stringValue = t.value[t.value.find('$)')+2]

            localTempToken = p.findall(stringValue)
            if localTempToken:
                for tokens in localTempToken[0].split():
                    self.CheckToken(t.value)

                    for cleanToken in self.testTokenList:
                        self.CheckSign(cleanToken)

        del self.testTokenList[:]
        return t

    def t_eof(self, t):
        # Get more input (Example)
        global counter
        if counter == 0:
            self.write_to_file(self.fileName, "\n------ PNUMBER: "+self.pNumber+" ------")
            self.write_to_file(self.fileName, "------ Warnings Start ------")
            self.write_to_file(self.fileName, self.errors)
            self.objStructure.CheckSurfaceRules()
            self.objStructure.CheckSealRule()
            self.write_to_file(self.fileName, self.errorText)
            self.write_to_file(self.fileName, "------ Warnings End ------\n")
            counter = counter + 1
            self.errors = ""
        else:
            counter = 0
        return None

    # Error handling rule
    def t_error(self, t):
        if not str(t.value[0]) == " ":
            self.write_to_file(self.fileName, "Illegal character " +str(t.value[0]))
        t.lexer.skip(1)

    def write_to_file(self, file, content):
        text_file = open("/atfchecker_data/output/"+file, "a")
        text_file.write(content+"\n")
        text_file.close()

    def CheckToken(self, token):
        tempList = self.CleanToken(token)
        if tempList:
            self.testTokenList.append(tempList)

        for iterToken in self.testTokenList:
            if not iterToken in self.tokenList:
                self.errorText += "Line:"+str(self.lexer.lineno)+" &#9 Token not recognized - "+str(iterToken)+"\n"

    def CheckSign(self, word):
        temp = word.split('-')
        finalTemp = list()
        finalSignList = list()
        signList = list()

        for splitWords in temp:
            iterItem = splitWords.split(':')
            for signs in iterItem:
                finalTemp.append(signs)

        for element in finalTemp:
            if '{' in element and '}' in element:
                if element.rfind('{') == 0:
                    finalSignList.append(element[element.rfind('{')+1:element.rfind('}')])
                    finalSignList.append(element[element.rfind('}')+1:])
                else:
                    finalSignList.append(element[:element.rfind('{')])
                    finalSignList.append(element[element.rfind('{')+1:element.rfind('}')])
            else:
                finalSignList.append(element)

        detected = False
        temp = ""

        if "(" in word and ")" in word and len(finalSignList) == 1:
            signList.append(finalSignList[0])

        if "(" in word and ")" in word:
            for signs in finalSignList:
                if "(" in signs:
                    temp += signs
                    detected = True
                elif detected and not ")" in signs:
                    temp += "-"+signs
                elif ")" in signs and detected:
                    temp += signs
                    detected = False
                    signList.append(temp)
                    temp = ""
                else:
                    signList.append(signs)
        else:
            for signs in finalSignList:
                signList.append(signs)

        for sign in signList:
            if not sign in self.signList:
                self.errorText += "Line:"+str(self.lexer.lineno)+" &#9 Sign not recognized - "+str(sign)+"\n"

    def LoadLanguageToMemory(self):
        for root, dirs, files in os.walk(self.databaseDirectoryPath+"/Token_Database"):
            for file_ in files:
                if self.languageFile in file_:
                    self.AddToList(self.databaseDirectoryPath, file_)

    def AddToList(self, dirPath, fileName):
        with open(dirPath+"/Token_Database/"+fileName) as f:
            for line in f:
                self.tokenList.append(line.rstrip())

        with open(dirPath+"/Sign_Database/"+fileName) as f:
            for line in f:
                self.signList.append(line.rstrip())

    def CleanToken(self, token):
        symbols = ['<','>','#','!','?','[',']','_']
        for symbol in symbols:
            if symbol in token:
                token = token.replace(symbol,'')

        if "{+" in token:
            if token.find("+") != 1:
                temp = token[:token.find("{+")]
                self.testTokenList.append(temp)

            temp = token[token.find("{+")+1:token.find("}")]
            self.testTokenList.append(temp)

            if token.find("}") != len(token)-1:
                temp = token[token.find("}")+1:]
                self.testTokenList.append(temp)

            return None

        return token
