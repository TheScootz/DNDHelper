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
        super().__init__(parent, xscrollcommand=self.scrollH.set, yscrollcommand=self.scrollV.set, **kwargs)
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
        self.bgpath = path
        self.background = ImageTk.PhotoImage(file=path)
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

class SetScaleDialog(tk.Toplevel):
    def __init__(self, master, mapbg, **kwargs):
        super().__init__(master, kwargs)

        self.setupCanvas(mapbg)

        # This section (incl. comments) is taken from the TkDocs tutorial
        self.protocol("WM_DELETE_WINDOW", self.dismiss) # intercept close button
        self.transient(master)   # dialog window is related to main
        self.wait_visibility() # can't grab until window appears, so we wait
        self.grab_set()        # ensure all input goes to our window
        self.wait_window()     # block until window is destroyed


    def setupCanvas(self, bgpath):
        bg = Image.open(bgpath)
        # Shrink the image if it's bigger than 1024 x 768
        if bg.width > 1024 or bg.height > 768:
            aspectratio = bg.width / bg.height
            # Figure out which dimension needs more shrinking
            w_over = max(bg.width - 1024, 0)
            h_over = max(bg.height - 768, 0)

            if (w_over > h_over):
                w_new = bg.width - w_over
                h_new = bg.height - (w_over / aspectratio)
            else:
                w_new = bg.width - (h_over * aspectratio)
                h_new = bg.height - h_over

            bg = bg.resize((int(w_new), int(h_new)))

        bg = ImageTk.PhotoImage(image=bg)
        self.canvas = tk.Canvas(self, width=bg.width(), height=bg.height())
        self.canvas.create_image(0, 0, image=bg, anchor='nw')
        self.canvas.grid(column=0, row=0)

    # Also from TkDocs
    def dismiss(self):
        self.grab_release()
        self.destroy()

class MapWidget(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.map = Map(self, width=800, height=600)
        self.map.grid(column=0, row=0, padx=10, pady=10, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.mapButtonContainer = ttk.Frame(self, width=800, height=120, style="BW.TFrame")
        self.mapButtonContainer.grid(column=0, row=2, padx=10, pady=10, sticky=tk.S)

        self.setBackgroundButton = ttk.Button(self.mapButtonContainer, text="Set Background", command=self.setBackground)
        self.addCharacterButton = ttk.Button(self.mapButtonContainer, text="Add Character")
        self.addAOEButton = ttk.Button(self.mapButtonContainer, text="Add Area of Effect", command=self.promptAOE)
        self.setBackgroundButton.grid(column=0, row=0, sticky=tk.W)
        self.addCharacterButton.grid(column=1, row=0)
        self.addAOEButton.grid(column=2, row=0, sticky=tk.E)
        ttk.Button(self.mapButtonContainer, text="Set Scale", command=self.setScale).grid(column=3, row=0)

    def setBackground(self, *args):
        imagepath = tk.filedialog.askopenfilename(filetypes=["{Image files} {.jpg .png .gif .bmp}"])
        if imagepath != "":
            self.map.setBackground(imagepath)

    def promptAOE(self, *args):
        self.map.bind("<1>", self.addAOE)

    def addAOE(self, event):
        aoe = Map.AOE(Map.RECTANGLE, (50, 100), (event.x, event.y))
        self.map.addAOE(aoe)

    def setScale(self, *args):
        dialog = Map.SetScaleDialog(self, self.map.bgpath)

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