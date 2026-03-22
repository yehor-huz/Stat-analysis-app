import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from prettytable import PrettyTable
from scipy import stats

class ReportWidget(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=None, **kwargs)
        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=1, weight=1)
        self.label = ttk.Label(self, text="Report").grid(column=0, row=0)
        self.text = scrolledtext.ScrolledText(self, background='lightgray')
        self.text.config(state="disabled")
        self.text.grid(column=0, row=1, sticky="NSEW")
    
    def putText(self, text):
        self.text.config(state="normal")
        self.text.delete('1.0', tk.END)
        self.text.insert(tk.END, text)
        self.text.config(state="disabled")
    
    def generateReport(self, df):
            if df is None or df.empty:
                return "No data available."

            table = PrettyTable()
            table.field_names = [
                "Feature", "Mean", "Median", "Min", "Max", 
                "Std Dev", "Skewness", "Kurtosis", 
                "W Stat", "p-value", "Normal?"
            ]
            
            table.align["Feature"] = "l"
            for field in table.field_names[1:]:
                table.align[field] = "r"
            table.float_format = ".4"

            for colName in df.columns:
                col_data = df[colName].dropna()
                if col_data.empty:
                    continue

                dataArr = col_data.to_numpy()
                mean_val = col_data.mean()
                median_val = col_data.median()
                min_val = col_data.min()
                max_val = col_data.max()
                std_val = col_data.std()
                skew_val = col_data.skew()
                kurtosis_val = col_data.kurtosis()

                if len(dataArr) >= 3:
                    W, p = stats.shapiro(dataArr)
                    isNormalyDistributed = "Yes" if p > 0.05 else "No"
                    p_str = f"{p:.4g}"
                else:
                    W = float('nan')
                    p_str = "N/A"
                    isNormalyDistributed = "N/A"
                table.add_row([
                    colName, 
                    mean_val, 
                    median_val, 
                    min_val, 
                    max_val, 
                    std_val, 
                    skew_val, 
                    kurtosis_val, 
                    W, 
                    p_str, 
                    isNormalyDistributed
                ])
                
            return table.get_string()
    
    def update(self, df=None):
        if df == None:
            self.putText("No data available.")
            return
        textReport = self.generateReport(df)
        self.putText(textReport)
        return


