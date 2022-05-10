import tkinter as tk
from tkinter import ttk

class CharacterWidget(ttk.Frame):

    def __init__(self, master, **kwargs):

        super().__init__(master, **kwargs)

        self.characterWidgetContainer = ttk.Frame(self, width=350, height=200)
        self.characterWidgetContainer.grid(column=3, row=2, padx=10, pady=10)

        self.tempvar = "~Character~"

        ttk.Label(self.characterWidgetContainer, text=self.tempvar).grid(column=3,row=1)


class Character():

    def __init__(self, cname, hp):

        self.name = cname
        self.con_hp = hp
        self.max_hp = hp
        self.hp = hp
        self.xp = 0
        self.abilities = {"STR":8,"DEX":8,"CON":8,"INT":8,"WIS":8,"CHA":8}
        self.statuses = {}
        self.sanity = None


    def printChara(self):

        print("~Character: "+self.name+"~")
        print(self.abilities)
        if self.sanity != None:
            print("Sanity: "+str(self.sanity)+"/20")
        print("Max Hitpoints: "+str(self.con_hp))
        print("Hitpoints: "+str(self.hp)+"/"+str(self.max_hp))
        print("XP: "+str(self.xp))
        if len(self.statuses) > 0:
            print(self.statuses)
        print()


    def rename(self,newname):
        self.name = newname


    def modScores(self,score,newValue):

        if newValue < 0:
            newValue = 0
        elif newValue > 30:
            newValue = 30
        self.abilities[score] = newValue


    def modAll(self, newscores):

        for a in self.abilities:
            self.abilities[a] = newscores.pop(0)


    def toggleSanity(self,newValue):

        if newValue == None:
            self.sanity = None
        elif newValue < 0:
            newValue = 0
        elif newValue > 30:
            newValue = 30
        self.sanity = newValue


    def modHP(self,adj):

        if self.hp + adj > self.max_hp:
            self.hp = self.max_hp
        elif self.hp + adj < 0:
            self.hp = 0
        else:
            self.hp += adj


    def modMaxHP(self,adj):

        if self.max_hp + adj > self.con_hp:
            self.max_hp = self.con_hp
        elif self.max_hp + adj < 0:
            self.max_hp = 0
        else:
            self.max_hp += adj

        if self.hp > self.max_hp:
            self.hp = self.max_hp


    def fullHeal(self):
        self.hp = self.maxhp


    def resetHP(self,heal):
        self.max_hp = self.con_hp
        if heal:
            self.hp = self.max_hp


    def modXP(self,adj):

        if self.xp + adj < 0:
            self.xp = 0
        else:
            self.xp += adj


    def addStatus(self,status,duration):

        self.statuses[status] = duration


    def updateStatuses(self):

        for s in self.statuses:
            if self.statuses[s] == inf:
                continue
            else:
                dur = self.statuses[s]-1
            if dur == 0:
                del(self.statuses[s])
            else:
                self.statuses[s] = dur
