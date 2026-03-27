import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk

from plotBuilder import PlotBuilderInterface

PLOTS = ["Histogram", "Scatter", "Pairplot"]

class PlotControllerWidget(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.builder = PlotBuilderInterface()
        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=1)
        
        self.textFrame = scrolledtext.ScrolledText(self, background='white')
        self.textFrame.grid(column=0, row=0, sticky="NSEW")
        
        self.state = tk.StringVar(self, value=PLOTS[0])
        
        self._build_radiobuttons()

    def _build_radiobuttons(self):
        self.textFrame.config(state="normal")
        
        self.textFrame.tag_configure("center", justify="center")
    
        for plotNames in PLOTS:
            rb = tk.Radiobutton(
                self.textFrame, 
                text=plotNames, 
                variable=self.state, 
                value=plotNames, 
                indicatoron=0,           
                background="light gray", 
                selectcolor="gray",      
                width=15,                
                command=self.throwEvent  
            )
            
            self.textFrame.window_create("end", window=rb)
            self.textFrame.insert("end", "\n\n", "center")
            
        self.textFrame.config(state="disabled")

    def throwEvent(self):
        self.event_generate("<<PlotSelected>>")

    def buildPlot(self, dataframe):
            state = self.state.get()
            if dataframe is None or dataframe.empty:
                print("DF is empty")
                return None

            if state == PLOTS[0]: 
                data = dataframe.iloc[:, 0]
                name = dataframe.columns[0]
                print(name)
                return self.builder.getHist(data, name)
                
            elif state == PLOTS[1]: 
                if len(dataframe.columns) < 2:
                    print("Not enough variables for scatter")
                    return None
                    
                data = [dataframe.iloc[:, 0], dataframe.iloc[:, 1]]
                names = [dataframe.columns[0], dataframe.columns[1]]
                return self.builder.getScatter(data, names)
                
            elif state == PLOTS[2]:
                return self.builder.getPairplot(dataframe)