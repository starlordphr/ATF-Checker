from collections import defaultdict
import re

class Structure(object):
    def __init__(self, fileName):
        self.pNumber = ""
        self.objectType = ""
        self.sealStatus = False
        self.surfaceList = list()
        self.columnCounter = 0
        self.fileName = fileName

    def IncrementColumnCounter(self):
        self.columnCounter = self.columnCounter + 1

    def ResetColumnCounter(self):
        self.columnCounter = 0

    def SetSurface(self, surfaceType):
        self.surfaceList.append(surfaceType)

    def SetObjectType(self, roughType):
        if "@tablet" in roughType:
            self.objectType = "TABLET"
        elif "bulla" in roughType:
            self.objectType = "BULLA"
        elif "prism" in roughType:
            self.objectType = "PRISM"
        elif "barrel" in roughType:
            self.objectType = "BARREL"
        elif "cylinder" in roughType:
            self.objectType = "CYLINDER"
        elif "brick" in roughType:
            self.objectType = "BRICK"
        elif "cone" in roughType:
            self.objectType = "CONE"
        elif "sealing" in roughType:
            self.objectType = "SEALING"
        elif "seal" in roughType:
            self.objectType = "SEAL"
        elif "composite" in roughType:
            self.objectType = "COMPOSITE"

    def ResetObjectType(self):
        self.objectType = ""

    def CheckSurfaceRules(self):
        surfaceRegex = re.compile("@surface [a-zA-Z0-9]+")
        specificSurfaceRegex = re.compile("@(obverse[\?]?|reverse[\?]?|top[\?]?|bottom[\?]?|left[\?]?|right[\?]?)")
        faceSurfaceRegex = re.compile("@face [a-zA-Z0-9]+")
        sealRegex = re.compile("@seal\s([A-Z]{1}|[0-9]+)?")

        surfaceList = filter(surfaceRegex.match, self.surfaceList)
        specificSurfaceList = filter(specificSurfaceRegex.match, self.surfaceList)
        faceSurfaceList = filter(faceSurfaceRegex.match, self.surfaceList)
        sealList = filter(sealRegex.match, self.surfaceList)

        if len(faceSurfaceList) > 0:
            self.write_to_file(self.fileName, "xxxxxxx> General Warning: Surface Type: face is not supported anymore.")

        if self.objectType == "BULLA":
            if len(surfaceList) > 0 and len(specificSurfaceList) > 0:
                self.write_to_file(self.fileName, "xxxxxxx> Bulla Warning: Both Generic Surface type (ex. @surface) and Specific Surface type (ex. @obverse), cannot be used together.")
        elif self.objectType == "PRISM":
            if len(specificSurfaceList) > 0:
                self.write_to_file(self.fileName, "xxxxxxx> Prism Warning: Specific Surface type (ex. @obverse) are not allowed.")
        elif self.objectType == "BARREL":
            if len(specificSurfaceList) > 0:
                self.write_to_file(self.fileName, "xxxxxxx> Barrel Warning: Specific Surface type (ex. @obverse) are not allowed.")
        elif self.objectType == "CYLINDER":
            if len(specificSurfaceList) > 0:
                self.write_to_file(self.fileName, "xxxxxxx> Cylinder Warning: Specific Surface type (ex. @obverse) are not allowed.")
        elif self.objectType == "BRICK":
            if len(specificSurfaceList) > 0:
                self.write_to_file(self.fileName, "xxxxxxx> Brick Warning: Specific Surface type (ex. @obverse) are not allowed.")
        elif self.objectType == "CONE":
            if len(surfaceList) > 2:
                self.write_to_file(self.fileName, "xxxxxxx> Cone Warning: More than 2 Generic Surfaces are not allowed.")
            if len(specificSurfaceList) > 0:
                self.write_to_file(self.fileName, "xxxxxxx> Cone Warning: Specific Surface type (ex. @obverse) are not allowed.")
        elif self.objectType == "SEALING":
            if len(surfaceList) > 1:
                self.write_to_file(self.fileName, "xxxxxxx> Sealing Warning: More than 1 Generic Surfaces are not allowed.")
            if len(specificSurfaceList) > 0:
                self.write_to_file(self.fileName, "xxxxxxx> Sealing Warning: Specific Surface type (ex. @obverse) are not allowed.")
            if len(sealList) < 1:
                self.write_to_file(self.fileName, "xxxxxxx> Sealing Warning: There should atleast be one Seal impression.")
        elif self.objectType == "SEAL":
            if len(surfaceList) > 1:
                self.write_to_file(self.fileName, "xxxxxxx> Seal Warning: More than 1 Generic Surfaces are not allowed.")
            if len(specificSurfaceList) > 0:
                self.write_to_file(self.fileName, "xxxxxxx> Seal Warning: Specific Surface type (ex. @obverse) are not allowed.")
            if len(sealList) > 0:
                self.write_to_file(self.fileName, "xxxxxxx> Seal Warning: There shouldn't be any Seal.")
        elif self.objectType == "COMPOSITE":
            if len(surfaceList) > 1:
                self.write_to_file(self.fileName, "xxxxxxx> Composite Warning: More than 1 Generic Surfaces are not allowed.")
            if len(specificSurfaceList) > 0:
                self.write_to_file(self.fileName, "xxxxxxx> Composite Warning: Specific Surface type (ex. @obverse) are not allowed.")
            if len(sealList) > 0:
                self.write_to_file(self.fileName, "xxxxxxx> Composite Warning: There shouldn't be any Seal.")
            if self.columnCounter > 0:
                self.write_to_file(self.fileName, "xxxxxxx> Composite Warning: Columns are not allowed.")

    def CheckSealRule(self):
        sealFound = False
        insideEnvelope = False
        idx = 0

        if self.objectType != "TABLET":
            for surfaceElement in self.surfaceList:
                if sealFound and "seal" not in surfaceElement:
                    self.write_to_file(self.fileName, "xxxxxxx> General Warning: Seal Impression should be at the end of the ATF.")

                if "seal" in surfaceElement:
                    sealFound = True

        elif self.objectType == "TABLET":
            while True:
                if idx > len(self.surfaceList)-1:
                    idx = 0
                    break

                if idx != len(self.surfaceList)-1 and "seal" in self.surfaceList[idx] and "envelope" not in self.surfaceList[idx+1] and "seal" not in self.surfaceList[idx+1]:
                    self.write_to_file(self.fileName, "xxxxxxx> Tablet General Warning: Seal Impression should be at the end of the ATF.")
                idx = idx + 1

    def write_to_file(self, file, content):
        text_file = open("/atfchecker_data/output/"+file, "a")
        text_file.write(content+"\n")
        text_file.close()
