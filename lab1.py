import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np

class StatApp(tk.Tk):
    def __init__(self, screenName = None, baseName = None, className = "Tk", useTk = True, sync = False, use = None):
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.geometry("1080x720")
        self.columnconfigure(0, weight=4)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)

        self.toolbar = tk.Menu(self)
        self.config(menu=self.toolbar)
        self.fileMenu = tk.Menu(self.toolbar, tearoff=False)
        self.toolbar.add_cascade(label="File", menu=self.fileMenu)

        self.fileMenu.add_command(label="Open", command=self._handleOpenFile)
        self.fileMenu.add_command(label="Generate Sample", command=self._handleSampleGeneration)
        self.fileMenu.add_command(label="Save report", command=self._saveReport)

        self.plotMenu = tk.Menu(self.toolbar, tearoff=False)
        self.toolbar.add_cascade(label="Plot", menu=self.plotMenu)
        self.plotMenu.add_command(label="Settings", command=self._handlePlot)

        #canvas for matplotplib
        self.canvas = tk.Frame(self, bg="lightgray")
        self.canvas.grid(column=0, columnspan=2, row=0, sticky="nsew")
        
        #side panel for controls
        self.sidePanel = tk.Frame(self, bg="gray")
        self.sidePanel.grid(column=2, row=0, sticky="nsew")

        self.sidePanel.columnconfigure(0, weight=1, pad=30)
        self.sidePanel.rowconfigure(0, weight=4, pad=30)
        self.sidePanel.rowconfigure(1, weight=1, pad=30)

        self.statText = tk.Text(self.sidePanel, width=1)
        self.statText.grid(column=0, row=0, sticky="nsew")

        self.nonLinearTransformator = ttk.Combobox(self.sidePanel, values=["None", "log", "Box-Cox", "Yeo-Johnson"], state="readonly")
        self.nonLinearTransformator.set("None")
        self.nonLinearTransformator.bind("<<ComboboxSelected>>", self._nonLinearTransformation)
        self.nonLinearTransformator.grid(column=0, row=1, sticky="ew")

    
    def _handleOpenFile(self):
        filepath = filedialog.askopenfilename()
        if filepath.endswith(".csv"):
            self.sample = pd.read_csv(filepath)
        else:
            extId = filepath.rfind(".")
            msg = f"Unfortunately, system does not support {filepath[extId:]}"
            messagebox.showerror(title="Extention error", message=msg)
            return
        #print(self.sample.head())
        #self._putText(self.sample.to_string())
   
    def _putText(self, text):
        self.statText.config(state="normal")
        self.statText.delete('1.0', tk.END)
        self.statText.insert(tk.END, text)
        self.statText.config(state="disabled")        
    
    def _handleSampleGeneration(self):
        return
    
    def _saveReport(self):
        return
    
    def _handlePlot(self):
        return
    
    def _nonLinearTransformation(self):
        return

app = StatApp()
app.mainloop()

