import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import numpy as np
import pandas as pd
from correlationMatrixWindow import CorrelationMatrixWindow
from nonLinearTransformerFrame import TRANSFORMATIONS, TransformerWidget
from partialCorrelationWindow import PartialCorrelationWindow
from plotControllerWidget import PlotControllerWidget
from reportFrame import ReportWidget
from selectSampleFrame import SampleSelectionWidget
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from table import ContingencyAnalysisWindow

class MainWindow(tk.Tk):
    def __init__(self, screenName = None, baseName = None, className = "Tk", useTk = True, sync = False, use = None):
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.geometry("1080x720")
        self.title("StatAnalysis")
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
        self.toolbar.add_cascade(label="Correlation", menu=self.corrMenu)
        self.corrMenu.add_command(label="Correlation Matrix", command=self.openCorrelationMatrixWindow)
        self.corrMenu.add_command(label="Partial Correlation", command=self.openPartialCorrelationWindow)
        self.corrMenu.add_command(label="Multy Correlation")

        self.corrMenu.add_command(label="Contingency Analysis", command=self.openContingencyAnalysisWindow)
        #sample
        self.sample = pd.DataFrame()
        #building main window
        #report window
        self.reportWidget = ReportWidget()
        self.reportWidget.grid(column=0, row=2, sticky="NSEW")
        self.reportWidget.update()
        #choose rows window
        self.selectionWidget = SampleSelectionWidget()
        self.selectionWidget.bind("<<ColumnSelected>>", self.updateViewColumnSelection)
        self.selectionWidget.grid(column=1, row=2, sticky="NSEW")
        #non linear transformer
        self.transformerWidget = TransformerWidget(self.sample)
        self.transformerWidget.bind("<<DataTransformed>>", self.updateViewNonLinear)
        self.transformerWidget.grid(column=1, row=1, sticky="NSEW")
        #plot builder and plot settings
        self.plotSelector = PlotControllerWidget(self)
        self.plotSelector.bind("<<PlotSelected>>", self.drawPlot)
        self.plotSelector.grid(column=1, row=0, sticky="NSEW")
        self.canvas = tk.Frame(self, bg="lightgray")
        self.canvas.grid(column=0, rowspan=2, row=0, sticky="nsew")

        self.mainloop()

    def handleOpenFile(self):
        filepath = filedialog.askopenfilename()
        if filepath.endswith(".csv"):
            self.sample = pd.read_csv(filepath)
            headers = self.sample.columns
            self.selectionWidget.update(headers)
            self.transformerWidget.update(self.sample)
        elif filepath.endswith(".txt"):
            self.sample = pd.read_csv(filepath, sep="\s+", dtype=np.float64)
            headers = self.sample.columns
            self.selectionWidget.update(headers)
            self.transformerWidget.update(self.sample)
        else:
            extId = filepath.rfind(".")
            msg = f"Unfortunately, system does not support {filepath[extId:]}"
            messagebox.showerror(title="Extention error", message=msg)
            return
        self.reportWidget.update(self.sample)
        return
    
    def updateViewNonLinear(self, event):
        self.sample = self.transformerWidget.get()
        self.reportWidget.update(self.sample)
        self.drawPlot(event)


    def updateViewColumnSelection(self, event):
        self.drawPlot(event)
        print(self.selectionWidget.getSelection())

    def drawPlot(self, event):
        columns = self.selectionWidget.getSelection()
        if len(columns) == 0: 
            return
        
        figure = self.plotSelector.buildPlot(self.sample[columns])
        
        if not figure:
            return
        
        for widget in self.canvas.winfo_children():
            widget.destroy()

        localCanvas = FigureCanvasTkAgg(figure, self.canvas)
        localCanvas.draw()
        localCanvas.get_tk_widget().pack(fill="both", expand=True)

    def openCorrelationMatrixWindow(self):
        matrixWin = CorrelationMatrixWindow(self.sample[self.selectionWidget.getSelection()], master=self)
    
    def openPartialCorrelationWindow(self):
        partialCorrWindow = PartialCorrelationWindow(df = self.sample, master = self)

    def openContingencyAnalysisWindow(self):
        selected_columns = self.selectionWidget.getSelection()
        
        if self.sample.empty:
            messagebox.showwarning(title="Warning", message="Load sample")
            return
            
        if len(selected_columns) != 2:
            messagebox.showwarning(
                title="Selection Error", 
                message="Load exactly two variables."
            )
            return
            
        col_x = selected_columns[0]
        col_y = selected_columns[1]
        
        contingency_win = ContingencyAnalysisWindow(df=self.sample, col_x=col_x, col_y=col_y, master=self)
        
        contingency_win.focus_set()



    
main = MainWindow()