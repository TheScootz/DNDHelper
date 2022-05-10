import tkinter as tk
from tkinter import ttk
import math
import os
import random
from PIL import Image, ImageTk

DEFAULT_BACKGROUND = "default.png"
COLORS = ["Aqua", "Aquamarine", "Blue", "BlueViolet", "Brown", "CadetBlue", "Chartreuse", "Chocolate", "Coral", "CornflowerBlue", "Crimson", "Cyan", "DeepPink", "DeepSkyBlue", "DodgerBlue", "FireBrick", "ForestGreen", "Fuchsia", "Gold", "GoldenRod", "Green", "GreenYellow", "HotPink", "LimeGreen", "Magenta", "Maroon", "OliveDrab", "Orange", "OrangeRed", "Orchid", "Peru", "Pink", "Plum", "PowderBlue", "Purple", "Red", "RoyalBlue", "Salmon", "Sienna", "SkyBlue", "SpringGreen", "Teal", "Turquoise", "Violet", "YellowGreen"]
DRAG_SENSITIVITY = 1

CIRCLE = 0
RECTANGLE = 1

class Map(tk.Canvas):
    def __init__(self, master, **kwargs):
        # Create canvas and its scrollbars
        self.scrollH = ttk.Scrollbar(master, orient=tk.HORIZONTAL)
        self.scrollV = ttk.Scrollbar(master, orient=tk.VERTICAL)
        super().__init__(master, xscrollcommand=self.scrollH.set, yscrollcommand=self.scrollV.set, **kwargs)
        self.scrollH["command"] = self.xview
        self.scrollV["command"] = self.yview
        self.scrollH.grid(column=0, row=1, sticky=(tk.W, tk.E))
        self.scrollV.grid(column=1, row=0, sticky=(tk.N, tk.S))

        self.setBackground(DEFAULT_BACKGROUND)
        self.tokens = []
        self.aoe = []
        self.colors = COLORS.copy()
        self.scale = 10 # Scale of the map represents pixels per foot
        self.activeElement = None
        random.shuffle(self.colors)

        # Listen for mouse down to start drag-scroll 
        self.bind("<Button-1>", self.logPos)
        self.tag_bind("background", "<B1-Motion>", self.dragScroll)
        # Listen for element move and delete events
        self.bind("<B1-Motion>", self.moveElement)
        self.tag_bind("background", "<Button-1>", lambda e: self.setActiveElement(None))

        self.testElements()

    def testElements(self):
        self.addToken(Token(2, 0, (250,350)))
        self.addToken(Token(2, 0, (67,324)))
        #self.removeToken(self.tokens[0])

        self.addAOE(AOE(CIRCLE, 6, (300,300)))
        self.addAOE(AOE(RECTANGLE, (10,10), (500,150)))

    def setBackground(self, path):
        self.bgpath = path
        self.background = ImageTk.PhotoImage(file=path)
        # Set the canvas size to the size of the image
        self.config(scrollregion=(0, 0, self.background.width(), self.background.height()))
        self.create_image(0, 0, image=self.background, anchor='nw', tag="background")

    def addToken(self, token):
        if token not in self.tokens:
            self.tokens.append(token)
        if token.color is None:
            token.color = self.getColor()

        pos_tl = [x-(token.radius*self.scale) for x in token.position]
        pos_br = [x+(token.radius*self.scale) for x in token.position]
        token.id = sid = self.create_oval(*pos_tl, *pos_br, fill=token.color, width=3, tag="token")

        # Listen for drag movement
        self.tag_bind(token.id, "<Button-1>", lambda e: self.setActiveElement(token))
        self.tag_bind(token.id, "<Button-3>", lambda e: self.removeElement(token))
        
        # Move tokens in front of AOEs
        try:
            self.tag_raise(token.id, "aoe")
        # No AOEs exist
        except tk.TclError: pass

    def addAOE(self, aoe):
        if aoe not in self.aoe:
            self.aoe.append(aoe)
        if aoe.color is None:
            aoe.color = self.getColor()
        
        if aoe.shape == CIRCLE:
            pos_tl = [x-(aoe.size*self.scale) for x in aoe.position]
            pos_br = [x+(aoe.size*self.scale) for x in aoe.position]
            aoe.id = sid = self.create_oval(*pos_tl, *pos_br, fill=aoe.color, tag="aoe")
        elif aoe.shape == RECTANGLE:
            pos_tl = (aoe.position[0]-(aoe.size[0]*self.scale)//2, aoe.position[1]-(aoe.size[1]*self.scale)//2)
            pos_br = (aoe.position[0]+(aoe.size[0]*self.scale)//2, aoe.position[1]+(aoe.size[1]*self.scale)//2)
            aoe.id = sid = self.create_rectangle(*pos_tl, *pos_br, fill=aoe.color, tag="aoe")

        # Listen for drag movement
        self.tag_bind(aoe.id, "<Button-1>", lambda e: self.setActiveElement(aoe))
        self.tag_bind(aoe.id, "<Button-3>", lambda e: self.removeElement(aoe))

        # Move AOEs behind tokens
        try:
            self.tag_lower(aoe.id, "token")
        # No tokens exist
        except tk.TclError: pass
        
    def addNextToken(self, event):
        pos = self.convertPos((event.x, event.y))
        #self.nextToken.position = pos
        self.addToken(Token(2, 0, pos))
        self.unbind("<ButtonRelease-1>", self.addTokenBind)
        self.master.hideMessage()

    def addNextAOE(self, event):
        pos = self.convertPos((event.x, event.y))
        self.nextAOE.position = pos
        self.addAOE(self.nextAOE)
        self.unbind("<ButtonRelease-1>", self.addAOEBind)
        self.master.hideMessage()

    def removeElement(self, element):
        if type(element) is Token:
            self.tokens.remove(element)
        elif type(element) is AOE:
            self.aoe.remove(element)
        
        self.colors.append(element.color)
        self.delete(element.id)

    def getColor(self):
        try:
            return self.colors.pop(0)
        # If we're out of colors, refresh them
        except IndexError:
            self.colors = COLORS.copy()
            random.shuffle(self.colors)
            return self.colors.pop(0)

    def logPos(self, event):
        self.lastPos = (event.x, event.y)

    def dragScroll(self, event):
        # We want to move opposite the mouse direction so we do old - new
        x_diff = round((self.lastPos[0] - event.x) * DRAG_SENSITIVITY)
        y_diff = round((self.lastPos[1] - event.y) * DRAG_SENSITIVITY)

        self.xview(tk.SCROLL, x_diff, tk.UNITS)
        self.yview(tk.SCROLL, y_diff, tk.UNITS)

        self.lastPos = (event.x, event.y)

    def convertPos(self, pos):
        x = self.canvasx(pos[0])
        y = self.canvasy(pos[1])
        return (x, y)

    def refresh(self):
        for t in self.tokens:
            self.delete(t.id)
            self.addToken(t)
        for a in self.aoe:
            self.delete(a.id)
            self.addAOE(a)

    def moveElement(self, event):
        if self.activeElement is None: return
        x_diff = event.x - self.lastPos[0]
        y_diff = event.y - self.lastPos[1]
        
        newX = self.activeElement.position[0] + x_diff
        newY = self.activeElement.position[1] + y_diff

        self.activeElement.position = (newX, newY)
        self.refresh()
        self.lastPos = (event.x, event.y)

    def setActiveElement(self, element):
        self.activeElement = element


        

class SetScaleDialog(tk.Toplevel):
    def __init__(self, master, mapCanvas, **kwargs):
        super().__init__(master, **kwargs)

        self.map = mapCanvas
        self.scale = self.map.scale
        self.setupCanvas(self.map.bgpath)

        # This section (incl. comments) is taken from the TkDocs tutorial
        self.protocol("WM_DELETE_WINDOW", self.dismiss) # intercept close button
        self.transient(master)   # dialog window is related to main
        self.wait_visibility() # can't grab until window appears, so we wait
        self.grab_set()        # ensure all input goes to our window
        self.wait_window()     # block until window is destroyed

    def setupCanvas(self, bgpath):
        self.bg = Image.open(bgpath)
        self.ratio = (1, 1) # How much the width and height have been scaled from the original
        # Shrink the image if it's bigger than 1024 x 768
        if not (self.bg.width > 1024 or self.bg.height > 768):
            aspectratio = self.bg.width / self.bg.height
            # Figure out which dimension needs more shrinking
            w_over = max(self.bg.width - 1024, 0)
            h_over = max(self.bg.height - 768, 0)

            if (w_over > h_over):
                w_new = self.bg.width - w_over
                h_new = self.bg.height - (w_over / aspectratio)
            else:
                w_new = self.bg.width - (h_over * aspectratio)
                h_new = self.bg.height - h_over

            self.ratio = (self.bg.width / w_new, self.bg.height / h_new)
            self.bg = self.bg.resize(size=(int(w_new), int(h_new)))

        self.bg = ImageTk.PhotoImage(self.bg)
        self.canvas = tk.Canvas(self, width=800, height=600, scrollregion=(0, 0, self.bg.width(), self.bg.height()))
        self.canvas.grid(column=0, row=0)
        self.canvas.create_image(0, 0, image=self.bg, anchor='nw')
        self.createGrid(self.scale)

        ttk.Label(self, text="Drag so that the grid squares cover 5 square feet").grid(column=0, row=1)
        ttk.Scale(self, orient=tk.HORIZONTAL, from_=10, to=100, value=self.scale, command=self.createGrid).grid(column=0, row=2, sticky=(tk.W, tk.E))
        ttk.Button(self, text="OK", command=self.dismiss).grid(column=0, row=3)

    # Code comes from https://stackoverflow.com/questions/34006302/how-to-create-a-grid-on-tkinter-in-python
    def createGrid(self, scale):
        self.scale = round(float(scale))
        w = self.canvas.winfo_width() # Get current width of canvas
        h = self.canvas.winfo_height() # Get current height of canvas
        self.canvas.delete('grid_line') # Will only remove the grid_line

        spacing = int(self.scale * 5)

        # Creates all vertical lines at intevals of spacing
        for i in range(0, w, spacing):
            self.canvas.create_line([(i, 0), (i, h)], tag='grid_line')

        # Creates all horizontal lines at intevals of spacing
        for i in range(0, h, spacing):
            self.canvas.create_line([(0, i), (w, i)], tag='grid_line')

    # Also from TkDocs
    def dismiss(self):
        self.map.scale = self.scale
        self.grab_release()
        self.destroy()


class AOEDialog(tk.Toplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.shape = tk.IntVar(self, 0)

        self.setup()

        # This section (incl. comments) is taken from the TkDocs tutorial
        self.protocol("WM_DELETE_WINDOW", self.dismiss) # intercept close button
        self.transient(master)   # dialog window is related to main
        self.wait_visibility() # can't grab until window appears, so we wait
        self.grab_set()        # ensure all input goes to our window
        self.wait_window()     # block until window is destroyed

    def setup(self):
        ttk.Label(self, text="Shape: ").grid(column=0, row=0, columnspan=2)
        ttk.Radiobutton(self, text="Circle", variable=self.shape, value=CIRCLE).grid(column=2, row=0)
        ttk.Radiobutton(self, text="Rectangle", variable=self.shape, value=RECTANGLE).grid(column=3, row=0)

        self.radius = tk.IntVar(self, 0)
        self.width = tk.IntVar(self, 0)
        self.height = tk.IntVar(self, 0)
        self.circleLabel = ttk.Label(self, text="Radius: ")
        self.circleEntry = ttk.Entry(self, width=2, justify=tk.CENTER, textvariable=self.radius)
        self.rectangleLabelW = ttk.Label(self, text="Width: ")
        self.rectangleEntryW = ttk.Entry(self, width=2, justify=tk.CENTER, textvariable=self.width)
        self.rectangleLabelH = ttk.Label(self, text="Height: ")
        self.rectangleEntryH = ttk.Entry(self, width=2, justify=tk.CENTER, textvariable=self.height)

        self.update(None)

        ttk.Button(self, text="Add", command=self.dismiss).grid(column=0, row=2, columnspan=4)

        self.bind("<ButtonRelease-1>", self.update)

    def update(self, event):
        if self.shape.get() == CIRCLE:
            self.rectangleLabelW.grid_remove()
            self.rectangleEntryW.grid_remove()
            self.rectangleLabelH.grid_remove()
            self.rectangleEntryH.grid_remove()
            self.circleLabel.grid(column=0, row=1, columnspan=2)
            self.circleEntry.grid(column=2, row=1)
        elif self.shape.get() == RECTANGLE:
            self.circleLabel.grid_remove()
            self.circleEntry.grid_remove()
            self.rectangleLabelW.grid(column=0, row=1)
            self.rectangleEntryW.grid(column=1, row=1)
            self.rectangleLabelH.grid(column=2, row=1)
            self.rectangleEntryH.grid(column=3, row=1)

    # Also from TkDocs
    def dismiss(self):
        if self.shape.get() == CIRCLE:
            size = self.radius.get()
        elif self.shape.get() == RECTANGLE:
            size = (self.width.get(), self.height.get())
        
        self.master.map.nextAOE = AOE(self.shape.get(), size)
        self.master.map.addAOEBind = self.master.map.bind("<ButtonRelease-1>", self.master.map.addNextAOE, add="+")
        self.master.showMessage("Click on the center of your area of effect.")
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
        self.addCharacterButton = ttk.Button(self.mapButtonContainer, text="Add Character", command=self.promptChar)
        self.addAOEButton = ttk.Button(self.mapButtonContainer, text="Add Area of Effect", command=self.promptAOE)
        self.setBackgroundButton.grid(column=0, row=0, sticky=tk.W)
        self.addCharacterButton.grid(column=1, row=0)
        self.addAOEButton.grid(column=2, row=0, sticky=tk.E)
        ttk.Button(self.mapButtonContainer, text="Set Scale", command=self.setScale).grid(column=3, row=0)

        self.message = ttk.Label(self)
        self.message.grid(column=0, row=3)

    def setBackground(self, *args):
        imagepath = tk.filedialog.askopenfilename(filetypes=["{Image files} {.jpg .png .gif .bmp}"])
        if imagepath != "":
            self.map.setBackground(imagepath)

    def promptChar(self, *args):
        self.map.addTokenBind = self.map.bind("<ButtonRelease-1>", self.map.addNextToken, add="+")

    def promptAOE(self, *args):
        dialog = AOEDialog(self)

    def setScale(self, *args):
        dialog = SetScaleDialog(self, self.map)

    def showMessage(self, message):
        self.message.config(text=message)

    def hideMessage(self):
        self.message.config(text="")
        

class Token:
    def __init__(self, radius, height, position=(0,0), color=None, oid=0):
        self.radius = radius
        self.height = height
        self.position = position
        self.color = color
        self.id = oid

class AOE:
    def __init__(self, shape, size, position=(0,0), color=None, oid=0):
        self.shape = shape
        self.size = size
        self.position = position
        self.color = color
        self.id = oid