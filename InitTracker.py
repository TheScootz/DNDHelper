import tkinter as tk
from tkinter import ttk

class ITrackerWidget(ttk.Frame):
    def __init__(self, master, **kwargs):

        super().__init__(master, **kwargs)

        self.initiativeTrackerWidgetContainer = ttk.Frame(self, width=250, height=200)
        self.initiativeTrackerWidgetContainer.grid(column=3, row=1, columnspan=6, padx=10, pady=10,sticky=(tk.W+tk.N,tk.N))

        self.initiativelist = ITracker(50)

        # ADDING CHARACTERS FOR DEMO
        self.initiativelist.addCharacter("Father Alaric",9)
        self.initiativelist.addCharacter("Cecyl",14)
        self.initiativelist.addCharacter("Matriarch Chessira",5)
        self.initiativelist.addCharacter("Lady Endette",15)
        self.initiativelist.addCharacter("Lord Voss",12)
        self.initiativelist.addCharacter("Clait'Horrox",26)
        self.initiativelist.addCharacter("Orair",18)

        self.initActive = "Inactive"
        self.thisTurn = None#self.initiativelist.initiative
        self.nextTurn = None#self.initiativelist.next

        self.startButton = ttk.Button(self.initiativeTrackerWidgetContainer, text="Start Initiative", command=self.makeInit)
        self.startButton.grid(column=0, row=2, columnspan=5, pady=5, sticky=tk.S)
        #self.addCharButton = ttk.Button(self.initiativeTrackerWidgetContainer, text="Add Character", command=self.makeInit)
        #self.addCharButton.grid(column=0, row=5, columnspan=5, pady=5, sticky=tk.S+tk.W)
        #self.remCharButton = ttk.Button(self.initiativeTrackerWidgetContainer, text="Remove Character", command=self.makeInit)
        #self.remCharButton.grid(column=5, row=5, columnspan=5, pady=5, sticky=tk.S+tk.E)
        self.stepButton = ttk.Button(self.initiativeTrackerWidgetContainer, text="Next Turn", command=self.stepInit)
        self.endButton = ttk.Button(self.initiativeTrackerWidgetContainer, text="End Initiative", command=self.endInit)


        self.activeLabel = ttk.Label(self.initiativeTrackerWidgetContainer, text="Initiative: "+self.initActive)
        self.activeLabel.grid(column=3,row=1,sticky=tk.S+tk.W)
        self.curTurnLabel = None
        self.nextTurnLabel = None


    #def addChar(self):



    def makeInit(self):
        self.initActive = "Active"
        self.initiativelist.startInitiative()
        self.activeLabel.config(text="Initiative: "+self.initActive)
        self.thisTurn = self.initiativelist.initiative
        self.nextTurn = self.initiativelist.next

        self.curTurnLabel = ttk.Label(self.initiativeTrackerWidgetContainer, text="Current Turn - "+str(self.initiativelist.getInit(self.thisTurn)))
        self.nextTurnLabel = ttk.Label(self.initiativeTrackerWidgetContainer, text="Next Turn - "+str(self.initiativelist.getInit(self.nextTurn)))
        self.curTurnLabel.grid(column=3,row=2,sticky=tk.W+tk.S)
        self.nextTurnLabel.grid(column=3,row=3,sticky=tk.W+tk.S)

        self.startButton.grid_remove()
        self.stepButton.grid(column=0, row=0, columnspan=5, pady=5,sticky = tk.W+tk.S)
        self.endButton.grid(column=4, row=0, columnspan=5, pady=5, sticky = tk.E+tk.S)


    def stepInit(self):
        self.initiativelist.stepInitiative()
        self.thisTurn = self.initiativelist.initiative
        self.nextTurn = self.initiativelist.next

        self.curTurnLabel.config(text="Current Turn - "+str(self.initiativelist.getInit(self.thisTurn)))
        self.nextTurnLabel.config(text="Next Turn - "+str(self.initiativelist.getInit(self.nextTurn)))


    def endInit(self):
        self.initActive = "Inactive"
        self.initiativelist.endInitiative()
        self.startButton.grid(column=0, row=2, columnspan=5, pady=5)
        self.activeLabel.config(text="Initiative: "+self.initActive)
        self.curTurnLabel.grid_remove()
        self.nextTurnLabel.grid_remove()
        self.stepButton.grid_remove()
        self.endButton.grid_remove()


class ITracker:

    def __init__(self, initiativeCount):
        self.initiativeList = {}
        self.initiative = None
        self.next = None
        self.initActive = False

        for i in range(1,initiativeCount+1):
            self.initiativeList[i] = []


    def getActive(self):
        if self.initActive == False:
            return "Inactive"
        else:
            return "Active"


    def getInit(self,initCheck):
        ret = str(initCheck)+": "
        rem = ['[',']','\'']
        st = str(self.initiativeList[initCheck])
        for c in rem:
            st = st.replace(c,"")
        ret+=st
        return ret


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
            elif i == self.next:
                print("\t\t<<",end="")
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
        self.initActive = True
        self.initiative = len(self.initiativeList)
        self.next = len(self.initiativeList)
        self.stepInitiative()
        self.stepInitiative()


    def stepInitiative(self):

        def nextTurn(curTurn):

            failsafe = False
            if curTurn-1 == 0:
                curTurn = len(self.initiativeList)
            else:
                curTurn -= 1

            while len(self.initiativeList[curTurn]) == 0:

                curTurn -= 1
                if curTurn == 0:
                    if failsafe == False:
                        failsafe = True
                        curTurn = len(self.initiativeList)
                    else:
                        return self.initiative

            return curTurn

        self.initiative = self.next
        self.next = nextTurn(self.initiative)



    def endInitiative(self):
        self.initActive = False
        self.initiative = None
        self.next = None


    def clearInitiative(self):
        self.endInitiative()
        del(self.initiativeList)
