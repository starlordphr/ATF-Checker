
class Qnumber(object):
    qlist = []
    qnumber = ""

    def __init__(self):
        self.qList = self.ReadQnumbers()

    def ReadQnumbers(self):
        qfile = open('/Library/WebServer/Documents/checker-script/SupportFiles/ValidQnumbers.txt', 'r')
        qlist = qfile.readlines()
        qfile.close()
        content = [x.strip() for x in qlist]
        return content

    def CheckQnumber(self, qnumber):
        if qnumber in self.qList:
            return True
        else:
            return False
