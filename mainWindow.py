import tkinter as tk
import pandas as pd
from nonLinearTransformerFrame import TRANSFORMATIONS
from reportFrame import ReportWidget

class MainWindow(tk.Tk):
    def __init__(self, screenName = None, baseName = None, className = "Tk", useTk = True, sync = False, use = None):
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.geometry("1080x720")
        self.columnconfigure(index=0, weight=3, uniform="cols")
        self.columnconfigure(index=1, weight=1, uniform="cols")
        self.rowconfigure(index=0, weight=1, uniform="rows")
        self.rowconfigure(index=1, weight=1, uniform="rows")
        self.rowconfigure(index=2, weight=1, uniform="rows")
        #toolbar
        self.toolbar = tk.Menu(self)
        self.config(menu=self.toolbar)
        
        self.fileMenu = tk.Menu(self.toolbar, tearoff=False)
        self.toolbar.add_cascade(label="File", menu=self.fileMenu)

        self.fileMenu.add_command(label="Open")
        self.fileMenu.add_command(label="Save report")

        self.corrMenu = tk.Menu(self.toolbar, tearoff=False)
        self.toolbar.add_cascade(label="Correlation", menu=self.corrMenu, state="disabled")
        self.corrMenu.add_command(label="Correlation Matrix")
        self.corrMenu.add_command(label="Partial Correlation")
        #sample
        self.sample = pd.DataFrame()
        self.currentTransformation = TRANSFORMATIONS[0]
        #building main window

        self.reportWidget = ReportWidget()
        self.reportWidget.grid(column=0, row=2, sticky="NSEW")
        self.reportWidget.update()

        self.mainloop()
    
main = MainWindow()