import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import warnings
import numpy as np
import pandas as pd
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
            "W", "p-value", "Normal?"
        ]
        
        table.align["Feature"] = "l"
        for field in table.field_names[1:]:
            table.align[field] = "r"

        def fmt(val):
            if pd.isna(val) or np.isinf(val):
                return "N/A"
            if val == 0:
                return "0.0000"
            if abs(val) >= 1e5 or abs(val) < 1e-4:
                return f"{val:.4e}"
            else:
                return f"{val:.4f}"

        for colName in df.columns:
            col_data = df[colName].dropna()
            
            if col_data.empty:
                continue

            dataArr = col_data.to_numpy()
            
            if not np.issubdtype(dataArr.dtype, np.number):
                continue

            n = len(dataArr)

            mean_val = fmt(col_data.mean())
            median_val = fmt(col_data.median())
            min_val = fmt(col_data.min())
            max_val = fmt(col_data.max())
            
            std_raw = col_data.std()
            std_val = fmt(std_raw)

            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=RuntimeWarning)
                
                skew_raw = col_data.skew()
                skew_val = fmt(skew_raw)
                
                kurt_raw = col_data.kurtosis()
                kurt_val = fmt(kurt_raw)

            if n >= 3 and pd.notna(std_raw) and std_raw > 0:
                if n > 5000:
                    test_data = np.random.choice(dataArr, 5000, replace=False)
                else:
                    test_data = dataArr
                    
                W, p = stats.shapiro(test_data)
                
                W_str = f"{W:.4f}"
                p_str = f"{p:.4g}" 
                isNormalyDistributed = "Yes" if p > 0.05 else "No"
            else:
                W_str = "N/A"
                p_str = "N/A"
                isNormalyDistributed = "N/A"

            table.add_row([
                colName, mean_val, median_val, min_val, max_val, 
                std_val, skew_val, kurt_val, 
                W_str, p_str, isNormalyDistributed
            ])
            
        return table.get_string()
    
    def update(self, df=None):
        textReport = self.generateReport(df)
        self.putText(textReport)
        return


