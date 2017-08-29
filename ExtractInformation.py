import os
import re
# import nltk
from collections import defaultdict

class ExtractInformation(object):
    def __init__(self, mainDirectory):
        self.mainDirectory = mainDirectory
        self.tokenList = list()
        self.signList = list()
        self.wordFreq = dict()
        self.signFreq = dict()

    def write_to_file(self, directory, fileName, content):
        with open(self.mainDirectory+directory+"/"+fileName, "w") as f:
            f.write(content)

    def InsertToken(self, line):
        for tokens in nltk.word_tokenize(line):
            self.tokenList.append(tokens)

    def InsertTokenMy(self, line, p):
        tempToken = p.findall(line)
        if tempToken:
            for tokens in tempToken[0].split():
                tempList = self.CleanToken(tokens)
                if tempList:
                    self.tokenList.append(tempList)

    def ListToString(self, type):
        temp = ""
        for word in type:
            temp = temp + word + "\n"

        return temp

    def DictToString(self, type):
        dicTemp = ""
        for w in sorted(type, key = type.get, reverse=True):
        #for key,value in self.wordFreq.iteritems():
            dicTemp = dicTemp + str(w) + "\t" +str(type[w]) + "\n"
        return dicTemp

    def CheckFrequency(self):

        for tokens in self.tokenList:
            self.GenerateSign(tokens)
            if tokens in self.wordFreq:
                self.wordFreq[tokens] = self.wordFreq[tokens] + 1
            else:
                self.wordFreq[tokens] = 1

    def CheckSignFrequency(self):

        for sign in self.signList:
            if sign in self.signFreq:
                self.signFreq[sign] = self.signFreq[sign] + 1
            else:
                self.signFreq[sign] = 1

    def CleanToken(self, token):
        symbols = ['<','>','#','!','?','[',']','_']
        for symbol in symbols:
            if symbol in token:
                token = token.replace(symbol,'')

        if "{+" in token:
            if token.find("+") != 1:
                temp = token[:token.find("{+")]
                self.tokenList.append(temp)

            temp = token[token.find("{+")+1:token.find("}")]
            self.tokenList.append(temp)

            if token.find("}") != len(token)-1:
                temp = token[token.find("}")+1:]
                self.tokenList.append(temp)

            return None

        return token

    def GenerateSign(self, word):
        temp = word.split('-')
        finalTemp = list()
        finalSignList = list()

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
            self.signList.append(finalSignList[0])

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
                    self.signList.append(temp)
                    temp = ""
                else:
                    self.signList.append(signs)
        else:
            for signs in finalSignList:
                self.signList.append(signs)

    def CreateTokens(self):
        p = re.compile("[0-9]+\'?. (.*)")
        database_dir = self.mainDirectory+"Processed_Database/"
        for fileName in os.listdir(database_dir):
            if not os.path.isdir(database_dir+fileName) and not fileName[0] == ".":
                temp = ""
                signTemp = ""
                dictTemp = ""
                signDictTemp = ""
                del self.tokenList
                del self.signList
                del self.wordFreq
                del self.signFreq
                self.tokenList = list()
                self.signList = list()
                self.wordFreq = dict()
                self.signFreq = dict()
                with open(database_dir+fileName) as fileHandle:
                    for line in fileHandle:
                        if line[0].isdigit():
                            #self.InsertTokenMy(re.sub("($(.)*$)","",line), p)
                            if "$)" in line and "($" in line:
                                self.InsertTokenMy(line[line.find('$)')+2], p)
                            else:
                                self.InsertTokenMy(line, p)
                self.CheckFrequency()
                self.CheckSignFrequency()
                self.tokenList = list(set(self.tokenList))
                self.signList = list(set(self.signList))
                temp = self.ListToString(self.tokenList)
                signTemp = self.ListToString(self.signList)
                dictTemp = self.DictToString(self.wordFreq)
                signDictTemp = self.DictToString(self.signFreq)
                self.write_to_file("Token_Database", fileName, temp)
                self.write_to_file("WordFreq_Database", fileName, dictTemp)
                self.write_to_file("Sign_Database", fileName, signTemp)
                self.write_to_file("SignFreq_Database", fileName, signDictTemp)
                print fileName, " Completed!"
            else:
                continue

    def PreProcessFiles(self):
        tempFileDict = dict()
        database_dir = self.mainDirectory + "Database/"
        for fileName in os.listdir(database_dir):
            tempFileDict[fileName] = 0

        for fileName in os.listdir(database_dir):
            if not os.path.isdir(database_dir+fileName) and not fileName[0] == ".":
                if tempFileDict[fileName] == 0:
                    tempFileDict[fileName] = 1
                    if fileName+" ?" in tempFileDict:
                        tempFileDict[fileName+" ?"] = 1
                        self.JoinFiles(fileName, fileName+" ?")
                    else:
                        self.JoinFiles(fileName)
                else:
                    continue

    def JoinFiles(self, file1, file2 = None):
        temp = ""
        # +"Darabase" removed
        with open(self.mainDirectory+"Database/"+file1, "r") as f:
            for line in f:
                temp += str(line)

        if not file2 == None:
            temp += "\n\n"

            # +"Database" removed
            with open(self.mainDirectory+"Database/"+file2, "r") as f:
                for line in f:
                    temp += str(line)

        self.write_to_file("Processed_Database", file1, temp)


    def ExtractTokens(self):
        database_dir = self.mainDirectory+"Database/"
        for fileName in os.listdir(database_dir):
            if not os.path.isdir(database_dir+fileName) and not fileName[0] == ".":
                temp = ""
                del self.tokenList
                del self.wordFreq
                self.tokenList = list()
                self.wordFreq = dict()
                with open(database_dir+fileName) as fileHandle:
                    for line in fileHandle:
                        if line[0].isdigit() and line[1] == ".":
                            self.InsertToken(line[2:])
                        elif line[0].isdigit() and line[2] == ".":
                            self.InsertToken(line[3:])
                self.tokenList = list(set(self.tokenList))
                temp = self.ListToString()
                self.write_to_file("Token_Database", fileName, temp)
                print fileName, " Completed!"
            else:
                continue



if __name__ == "__main__":
    path = raw_input("Database path: ")
    if path == "":
        objExtract = ExtractInformation("/Volumes/cdli_www_2/transfers/cdlicore/atfchecker_helper/")
    else:
        objExtract = ExtractInformation(path)
    objExtract.PreProcessFiles()
    objExtract.CreateTokens()
    objExtract.ExtractTokens()
