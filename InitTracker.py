import tkinter as tk
from tkinter import ttk

class ITrackerWidget(ttk.Frame):
    def __init__(self, master, **kwargs):

        super().__init__(master, **kwargs)

        self.initiativeTrackerWidgetContainer = ttk.Frame(self, width=250, height=200)
        self.initiativeTrackerWidgetContainer.grid(column=3, row=1, columnspan=5, padx=10, pady=10,sticky=(tk.W+tk.N,tk.N))

        self.initiativelist = ITracker(30)

        self.initActive = self.initiativelist.initActive
        self.thisTurn = self.initiativelist.initiative
        self.nextTurn = self.initiativelist.next

        #self.stepButton = ttk.Button(self.initiativeTrackerWidgetContainer, text="Next Turn")
        ttk.Button(self.initiativeTrackerWidgetContainer, text="Start Initiative", command=self.initiativelist.startInitiative()).grid(column=0, row=2, columnspan=5, pady=5)

        ttk.Label(self.initiativeTrackerWidgetContainer, text="Initiative: "+self.initiativelist.getActive()).grid(column=3,row=1)
        if self.initActive == True:
            ttk.Label(self.initiativeTrackerWidgetContainer, text="Current Turn: "+str(self.initiativelist.getInit(self.thisTurn))).grid(column=3,row=2)
            ttk.Label(self.initiativeTrackerWidgetContainer, text="Next Turn: "+str(self.initiativelist.getInit(self.nextTurn))).grid(column=3,row=3)


    def makeInit(self,iCount):
        return ITracker(iCount)



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
        #print("TEST")
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
