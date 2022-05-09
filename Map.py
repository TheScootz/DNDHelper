import tkinter as tk
from tkinter import ttk
import os
import random
from PIL import Image, ImageTk

DEFAULT_BACKGROUND = "default.png"
COLORS = ["red", "cyan", "blue", "purple", "magenta", "orange", "maroon", "green"]

CIRCLE = 0
RECTANGLE = 1

class Map(tk.Canvas):
    def __init__(self, parent, **kwargs):
        # Create canvas and its scrollbars
        self.scrollH = ttk.Scrollbar(parent, orient=tk.HORIZONTAL)
        self.scrollV = ttk.Scrollbar(parent, orient=tk.VERTICAL)
        super().__init__(parent, kwargs, xscrollcommand=self.scrollH.set, yscrollcommand=self.scrollV.set)
        self.scrollH["command"] = self.xview
        self.scrollV["command"] = self.yview
        self.scrollH.grid(column=0, row=1, sticky=(tk.W, tk.E))
        self.scrollV.grid(column=1, row=0, sticky=(tk.N, tk.S))

        self.setBackground(DEFAULT_BACKGROUND)
        self.tokens = []
        self.aoe = []
        self.colors = COLORS.copy()
        random.shuffle(self.colors)

        self.testTokens()

    def testTokens(self):
        self.addToken(Token(50, 0, (250,350)))
        self.addToken(Token(30, 0, (67,324)))
        #self.removeToken(self.tokens[0])

        self.addAOE(AOE(CIRCLE, 200, (300,300)))
        self.addAOE(AOE(RECTANGLE, (100,200), (500,10)))

    def setBackground(self, path):
        self.background = ImageTk.PhotoImage(Image.open(path))
        # Set the canvas size to the size of the image
        self.config(scrollregion=(0, 0, self.background.width(), self.background.height()))
        self.create_image(0, 0, image=self.background, anchor='nw')

    def addToken(self, token):
        if token in self.tokens: return
        self.tokens.append(token)
        token.color = self.getColor()

        pos_tl = [x-token.radius for x in token.position]
        pos_br = [x+token.radius for x in token.position]
        token.id = self.create_oval(*pos_tl, *pos_br, fill=token.color, width=5, tag="token")
        try:
            self.tag_raise(token.id, "aoe")
        # No AOEs exist
        except tk.TclError: pass

    def removeToken(self, token):
        try:
            self.tokens.remove(token)
        except ValueError:
            print("Token does not exist in the map.")
            return
            
        self.colors.append(token.color)
        self.delete(token.id)

    def addAOE(self, aoe):
        if aoe in self.aoe: return
        self.aoe.append(aoe)
        aoe.color = self.getColor()
        
        if aoe.shape == CIRCLE:
            pos_tl = [x-aoe.size for x in aoe.position]
            pos_br = [x+aoe.size for x in aoe.position]
            aoe.id = self.create_oval(*pos_tl, *pos_br, fill=aoe.color, tag="aoe")
        elif aoe.shape == RECTANGLE:
            pos_tl = aoe.position
            pos_br = (aoe.position[0]+aoe.size[0], aoe.position[1]+aoe.size[1])
            aoe.id = self.create_rectangle(*pos_tl, *pos_br, fill=aoe.color, tag="aoe")
        try:
            self.tag_lower(aoe.id, "token")
        # No tokens exist
        except tk.TclError: pass

    def removeAOE(self, aoe):
        try:
            self.aoe.remove(aoe)
        except ValueError:
            print("aoe does not exist in the map.")
            return

        colors.append(aoe.color)
        self.delete(aoe.id)

    def getColor(self):
        try:
            return self.colors.pop(0)
        # If we're out of colors, refresh them
        except IndexError:
            self.colors = COLORS.copy()
            random.shuffle(self.colors)
            return self.colors.pop(0)

class Token:
    def __init__(self, radius, height, position, color="white", oid=0):
        self.radius = radius
        self.height = height
        self.position = position
        self.color = color
        self.id = oid

class AOE:
    def __init__(self, shape, size, position, color="white", oid=0):
        self.shape = shape
        self.size = size
        self.position = position
        self.color = color
        self.id = oid