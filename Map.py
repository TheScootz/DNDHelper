import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk

DEFAULT_BACKGROUND = "default.png"

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

    def setBackground(self, path):
        self.background = ImageTk.PhotoImage(Image.open(path))
        self.config(scrollregion=(0, 0, self.background.width(), self.background.height()))
        self.create_image(0, 0, image=self.background, anchor='nw')

    def addToken(self, token):
        if token not in self.tokens:
            self.tokens.append(token)

    def removeToken(self, token):
        try:
            self.tokens.remove(token)
        except ValueError:
            print("Token does not exist in the map.")

    def addAOE(self, AOE):
        if AOE not in self.AOE:
            self.AOE.append(token)

    def removeAOE(self, AOE):
        try:
            self.AOE.remove(AOE)
        except ValueError:
            print("AOE does not exist in the map.")

class Token:
    def __init__(self, size, height, position):
        self.size = size
        self.height = height
        self.position = position

class AOE:
    def __init__(self, shape, size, center):
        self.shape = shape
        self.size = size
        self.center = center