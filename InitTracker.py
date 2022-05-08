class ITracker:

    def __init__(self, initiativeCount):
        self.initiativeList = {}
        self.initiative = None

        for i in range(1,initiativeCount+1):
            self.initiativeList[i] = []


    def printInit(self):

        iList = self.initiativeList
        for i in reversed(iList):
            print(i,end=" ")
            if len(iList[i]) != 0:
                for c in iList[i]:
                    if c == iList[i][len(iList[i])-1]:
                        print(c,end="")
                    else:
                        print(c,end=", ")
            if i == self.initiative:
                print("\t\t<",end="")
            print()


    def addCharacter(self, newChar, initCount):
        self.initiativeList[initCount].append(newChar)


    def removeCharacter(self,remChar,charInit):

        if len(self.initiativeList[charInit]) == 1:
            self.initiativeList[charInit] = []
        else:
            temp = self.initiativeList[charInit]
            self.initiativeList[charInit] = []
            for c in temp:
                if c != remChar:
                    self.initiativeList[charInit].append(c)


    def startInitiative(self):
        self.initiative = len(self.initiativeList)


    def stepInitiative(self):

        if self.initiative-1 == 0:
            self.startInitiative()
        else:
            self.initiative -= 1
            
        while len(self.initiativeList[self.initiative]) == 0:

            self.initiative -= 1
            if self.initiative == 0:
                self.startInitiative()



    def endInitiative(self):
        self.initiative = None


    def clearInitiative(self):
        del(self.initiativeList)
