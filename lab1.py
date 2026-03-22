import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib as plt
import pandas as pd
import numpy as np
from scipy import stats

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
        self.sidePanel.rowconfigure(0, weight=2, pad=30)
        self.sidePanel.rowconfigure(1, weight=1, pad=30)

        self.statText = tk.Text(self.sidePanel, width=1)
        self.statText.grid(column=0, row=0, sticky="nsew")

        self.nonLinearTransformer = ttk.Combobox(self.sidePanel, values=["None", "log", "Box-Cox", "Yeo-Johnson"], state="readonly")
        self.nonLinearTransformer.set("None")
        self.nonLinearTransformer.bind("<<ComboboxSelected>>", self._nonLinearTransformation)
        self.nonLinearTransformer.grid(column=0, row=1, sticky="ew")

        #sample
        self.sample = pd.DataFrame()
    
    def _handleOpenFile(self):
        filepath = filedialog.askopenfilename()
        if filepath.endswith(".csv"):
            self.sample = pd.read_csv(filepath)
        else:
            extId = filepath.rfind(".")
            msg = f"Unfortunately, system does not support {filepath[extId:]}"
            messagebox.showerror(title="Extention error", message=msg)
            return
        self._drawPlot()
        self._putReport()
   
    def _putText(self, text):
        self.statText.config(state="normal")
        self.statText.delete('1.0', tk.END)
        self.statText.insert(tk.END, text)
        self.statText.config(state="disabled")

    def _putReport(self):
        text = self._describeData()
        self._putText(text)
    
    def _handleSampleGeneration(self):
        weibullSettings = tk.Toplevel(self)
        weibullSettings.geometry("420x420")
        weibullSettings.title("Weibull Sample Generation")
        weibullSettings.columnconfigure(index=0, weight=1)
        weibullSettings.columnconfigure(index=1, weight=1)
        weibullSettings.columnconfigure(index=2, weight=1)
        weibullSettings.columnconfigure(index=3, weight=1)
        weibullSettings.rowconfigure(index=0, weight=2)
        weibullSettings.rowconfigure(index=1, weight=1)
        weibullSettings.rowconfigure(index=2, weight=1)

        tk.Label(weibullSettings, text="Choose k parameter and size of 1D sample (n)").grid(column=0, row=0, columnspan=4)

        n = tk.DoubleVar(value=10.0)
        k = tk.DoubleVar(value=3.6)

        kLabel = tk.Label(weibullSettings, text="k")
        kEntry = tk.Entry(weibullSettings, textvariable=k)
        kLabel.grid(column=0, row=1, sticky='ew')
        kEntry.grid(column=1, row=1, sticky='ew')

        nLabel = tk.Label(weibullSettings, text="n")
        nEntry = tk.Entry(weibullSettings, textvariable=n)
        nLabel.grid(column=2, row=1, sticky='ew')
        nEntry.grid(column=3, row=1, sticky='ew')

        def submit():
            nVar = n.get()
            kVar = k.get()
            values = np.random.weibull(a=kVar, size=int(nVar))
            self.sample = pd.DataFrame()
            self.sample['X'] = pd.Series(values)
            self._putReport()
            self._drawPlot()
            weibullSettings.destroy()
        
        tk.Button(weibullSettings, text="Generate", command=submit).grid(column=0, row=2, columnspan=4)

        return
    
    def _describeData(self):
        colName = self.sample.columns[0]
        dataArr = self.sample[colName].to_numpy()
        W, p = stats.shapiro(dataArr)
        isNormalyDistributed = "Yes" if p > 0.05 else "No"
        report = [
            "REPORT",
            "-" * 30,
            f"Mean               : {self.sample[colName].mean():.4f}",
            f"Median             : {self.sample[colName].median():.4f}",
            f"Min                : {self.sample[colName].min():.4f}",
            f"Max                : {self.sample[colName].max():.4f}",
            f"Std Dev            : {self.sample[colName].std():.4f}",
            f"Skewness           : {self.sample[colName].skew():.4f}",
            f"Kurtosis           : {self.sample[colName].kurtosis():.4f}",
            "-" * 30,
            "SHAPIRO-WILK TEST",
            f"W Statistic        : {W:.4f}",
            f"p-value            : {p:.4g}",
            f"Is Normal?         : {isNormalyDistributed}",
            "-" * 30
        ]
        
        fullText = "\n".join(report)
        return fullText
    
    def _saveReport(self):
        print("Report saved somewhere! Good luck finding it")
        return
    
    def _handlePlot(self):
        plotSettings = tk.Toplevel(self)
        plotSettings.geometry("420x420")
        plotSettings.title("Plot settings")
        plotSettings.columnconfigure(index=0, weight=1)
        plotSettings.columnconfigure(index=1, weight=1)
        plotSettings.rowconfigure(index=0, weight=2)
        plotSettings.rowconfigure(index=1, weight=1)
        plotSettings.rowconfigure(index=2, weight=1)

        tk.Label(plotSettings, text="Choose bin parameter").grid(column=0, row=0, columnspan=2)

        binVar = tk.DoubleVar(value=10.0)

        binLabel = tk.Label(plotSettings, text="k")
        binLabel.grid(column=0, row=1, sticky='ew') 
        binEntry = tk.Entry(plotSettings, textvariable=binVar)
        binEntry.grid(column=1, row=1, sticky='ew')

        def submit():
            bins = binEntry.get()
            plotSettings.destroy()
            self._drawPlot(int(bins))
        tk.Button(plotSettings, text="Apply", command=submit).grid(column=0, row=2, columnspan=2)
        return
    
    def _drawPlot(self, binsUser = 10):
        if self.sample.empty:
            return
        for widget in self.canvas.winfo_children():
            widget.destroy()

        colName = self.sample.columns[0]
        dataArr = self.sample[colName].to_numpy()
        
        figure = Figure(dpi=100)
        plot = figure.subplots()
        plot.hist(dataArr, bins = binsUser, density = True)
        plot.set_xlabel(colName)
        plot.set_ylabel("Density")

        localCanvas = FigureCanvasTkAgg(figure, self.canvas)
        localCanvas.draw()
        
        localCanvas.get_tk_widget().pack(fill="both", expand=True)


    def _nonLinearTransformation(self, event):
        if self.sample.empty:
            return
        colName = self.sample.columns[0]
        dataArr = self.sample[colName].to_numpy()
        state = self.nonLinearTransformer.get()
        if state == "None":
            return
        if state == "log":
            dataArr = np.log(dataArr)
        elif state == "Box-Cox":
            dataArr, lmbda = stats.boxcox(dataArr)
        elif state == "Yeo-Johnson":
            dataArr, lmbda = stats.yeojohnson(dataArr)
        print(dataArr)
        self.sample[colName] = pd.Series(dataArr)
        self._drawPlot()
        self._putReport()
        return

app = StatApp()
app.mainloop()

