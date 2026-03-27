import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
from nonLinearTransformerFrame import TRANSFORMATIONS
from reportFrame import ReportWidget
from selectSampleFrame import SampleSelectionWidget

class MainWindow(tk.Tk):
    def __init__(self, screenName = None, baseName = None, className = "Tk", useTk = True, sync = False, use = None):
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.geometry("1080x720")
        self.columnconfigure(index=0, weight=4, uniform="cols")
        self.columnconfigure(index=1, weight=1, uniform="cols")
        self.rowconfigure(index=0, weight=1, uniform="rows")
        self.rowconfigure(index=1, weight=1, uniform="rows")
        self.rowconfigure(index=2, weight=1, uniform="rows")
        #toolbar
        self.toolbar = tk.Menu(self)
        self.config(menu=self.toolbar)
        
        self.fileMenu = tk.Menu(self.toolbar, tearoff=False)
        self.toolbar.add_cascade(label="File", menu=self.fileMenu)

        self.fileMenu.add_command(label="Open", command=self.handleOpenFile)
        self.fileMenu.add_command(label="Save report")

        self.corrMenu = tk.Menu(self.toolbar, tearoff=False)
        self.toolbar.add_cascade(label="Correlation", menu=self.corrMenu, state="disabled")
        self.corrMenu.add_command(label="Correlation Matrix")
        self.corrMenu.add_command(label="Partial Correlation")
        #sample
        self.sample = pd.DataFrame()
        self.currentTransformation = TRANSFORMATIONS[0]
        #building main window
        #report window
        self.reportWidget = ReportWidget()
        self.reportWidget.grid(column=0, row=2, sticky="NSEW")
        self.reportWidget.update()
        #choose rows window
        self.selectionWidget = SampleSelectionWidget()
        self.selectionWidget.grid(column=1, row=2, sticky="NSEW")


        self.mainloop()

    def handleOpenFile(self):
        filepath = filedialog.askopenfilename()
        if filepath.endswith(".csv"):
            self.sample = pd.read_csv(filepath)
            headers = self.sample.columns
            self.selectionWidget.update(headers)
        else:
            extId = filepath.rfind(".")
            msg = f"Unfortunately, system does not support {filepath[extId:]}"
            messagebox.showerror(title="Extention error", message=msg)
            return
        self.reportWidget.update(self.sample)
        return
    
main = MainWindow()