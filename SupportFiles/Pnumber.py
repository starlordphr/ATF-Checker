
class Pnumber(object):
    oldPlist = []
    newPlist = []
    plist = []
    pnumber = 0

    def __init__(self):
        self.found = False
        self.pList = self.ReadPnumbers()
        self.oldPlist, self.newPlist = self.ReadPMap()

    def ReadPnumbers(self):
        pfile = open('SupportFiles/ValidPnumbers.txt', 'r')
        plist = pfile.readlines()
        pfile.close()
        content = [x.strip() for x in plist]
        formatContent = self.FormatPnumber(content)
        return formatContent

    def ReadPMap(self):
        temp = []
        oldPlist = []
        newPlist = []
        with open("SupportFiles/PnumberMap.txt") as file:
            for line in file:
                temp = line.split()
                oldPlist.append(temp[0].strip())
                newPlist.append(temp[1].strip())
        file.close()

        return oldPlist, newPlist

    def FormatPnumber(self, plist):
        formatPlist = []
        for pnumber in plist:
            stringBuilder = "P"
            length = len(pnumber)
            for i in range(1,7-length):
                stringBuilder = stringBuilder+"0"

            stringBuilder = stringBuilder + pnumber
            formatPlist.append(stringBuilder)

        return formatPlist

    def CheckPnumber(self, pnumber):
        if pnumber in self.pList:
            return True
        else:
            return False

    def CheckPMap(self, pnumber):
        foundMap = False

        if pnumber in self.oldPlist:
            foundMap = True

        if foundMap:
            index = self.oldPlist.index(pnumber)
            self.write_to_file("Replace Old Pnumber : "+pnumber+" with New Pnumber : "+self.newPlist[index])
            return self.newPlist[index], True
        else:
            if(self.CheckPnumber(pnumber)):
                return pnumber, True
            else:
                return pnumber, False

    def write_to_file(self, content):
        text_file = open("Output.txt", "a")
        text_file.write(content+"\n")
        text_file.close()
