import tkinter as tk
import pandas as pd

from correlationTypeWidget import TypeWidget
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CorrelationMatrixWindow(tk.Toplevel):
    def __init__(self, sample, master = None, **kwargs):
        super().__init__(master,**kwargs)
        self.geometry("1080x720")
        self.title("Correlation Matrix")
        self.columnconfigure(index=0, weight=4, uniform="cols")
        self.columnconfigure(index=1, weight=1, uniform="cols")
        self.rowconfigure(index=0, weight=1, uniform="rows")
        self.rowconfigure(index=1, weight=1, uniform="rows")
        self.rowconfigure(index=2, weight=1, uniform="rows")

        self.sample = sample

        #radiobutton to choose between linear and non linear relation and correlation type
        self.typeWidget = TypeWidget(master = self)
        self.typeWidget.bind("<<TypeSelected>>", self.handleCorrelation)
        self.typeWidget.grid(column=1, row=0, rowspan=2, sticky="NSEW")

        self.canvas = tk.Frame(self, bg="lightgray")
        self.canvas.grid(column=0, rowspan=2, row=0, sticky="nsew")

    def handleCorrelation(self, event):
            for widget in self.canvas.winfo_children():
                widget.destroy()
                
            fig = self.typeWidget.getCorrMatrix(self.sample)
            
            if fig is not None:
                canvas = FigureCanvasTkAgg(fig, master=self.canvas)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def updateSample(self, sample):
        self.sample = sample
        self.handleCorrelation()