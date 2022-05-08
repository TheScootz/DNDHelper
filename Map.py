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
        self.AOE = []

        random.shuffle(COLORS)
        self.testTokens()

    def testTokens(self):
        self.addToken(Token(50, 10, (50,50)))
        self.addToken(Token(30, 3, (67,324)))
        #self.removeToken(self.tokens[0])

    def setBackground(self, path):
        self.background = ImageTk.PhotoImage(Image.open(path))
        # Set the canvas size to the size of the image
        self.config(scrollregion=(0, 0, self.background.width(), self.background.height()))
        self.create_image(0, 0, image=self.background, anchor='nw')

    def addToken(self, token):
        if token in self.tokens: return

        self.tokens.append(token)
        token.id = self.create_oval(*token.position, *[x+token.size for x in token.position], fill=COLORS.pop(0), width=5)

    def removeToken(self, token):
        try:
            self.tokens.remove(token)
        except ValueError:
            print("Token does not exist in the map.")
            return

        self.delete(token.id)

    def addAOE(self, AOE):
        if AOE not in self.AOE:
            self.AOE.append(token)

    def removeAOE(self, AOE):
        try:
            self.AOE.remove(AOE)
        except ValueError:
            print("AOE does not exist in the map.")
            return

class Token:
    def __init__(self, size, height, position):
        self.size = size
        self.height = height
        self.position = position
        self.color = "white"
        self.id = 0

class AOE:
    def __init__(self, shape, size, center):
        self.shape = shape
        self.size = size
        self.center = center
        self.color = "white"
        self.id = 0