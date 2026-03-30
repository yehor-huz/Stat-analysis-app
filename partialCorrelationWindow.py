import tkinter as tk
from tkinter import ttk, scrolledtext
import numpy as np
import pandas as pd

from partialCorrelationCalculator import PartialCorrelationCalculator

class PartialCorrelationWindow(tk.Toplevel):
    
    def __init__(self, df: pd.DataFrame, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.df = df
        self.numeric_cols = self.df.select_dtypes(include=np.number).columns.tolist()
        
        self.title("Clear correlation coeficient")
        self.geometry("850x400")
        self.minsize(700, 350)
        
        self.columnconfigure(0, weight=1, uniform="col")
        self.columnconfigure(1, weight=1, uniform="col")
        self.columnconfigure(2, weight=2)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        
        self._build_ui()
        self._populate_listbox()
        self.generate_report() 

    def _build_ui(self):
        varXFrame = tk.Frame(self)
        varXFrame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="EW")
        tk.Label(varXFrame, text="X:").pack(anchor="w")
        self.comboX = ttk.Combobox(varXFrame, values=self.numeric_cols, state="readonly")
        if len(self.numeric_cols) > 0: self.comboX.current(0)
        self.comboX.pack(fill="x")
        self.comboX.bind("<<ComboboxSelected>>", self._on_combobox_change)

        varYFrame = tk.Frame(self)
        varYFrame.grid(row=0, column=1, padx=10, pady=(10, 5), sticky="EW")
        tk.Label(varYFrame, text="Y:").pack(anchor="w")
        self.comboY = ttk.Combobox(varYFrame, values=self.numeric_cols, state="readonly")
        if len(self.numeric_cols) > 1: self.comboY.current(1)
        self.comboY.pack(fill="x")
        self.comboY.bind("<<ComboboxSelected>>", self._on_combobox_change)

        frameCovar = tk.Frame(self)
        frameCovar.grid(row=1, column=0, columnspan=2, padx=10, pady=(5, 10), sticky="NSEW")
        
        tk.Label(frameCovar, text="Exclude influence:").pack(anchor="w")
        
        scroll_y = tk.Scrollbar(frameCovar)
        scroll_y.pack(side="right", fill="y")
        
        self.listbox = tk.Listbox(frameCovar, selectmode=tk.MULTIPLE, yscrollcommand=scroll_y.set)
        self.listbox.pack(side="left", fill="both", expand=True)
        scroll_y.config(command=self.listbox.yview)
        
        self.listbox.bind("<<ListboxSelect>>", lambda e: self.generate_report())

        self.report_text = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.report_text.grid(row=0, column=2, rowspan=2, padx=10, pady=10, sticky="NSEW")

    def _on_combobox_change(self, event):
        self._populate_listbox()
        self.generate_report()

    def _populate_listbox(self):
        x_val = self.comboX.get()
        y_val = self.comboY.get()
        
        selected_items = [self.listbox.get(i) for i in self.listbox.curselection()]
        
        self.listbox.delete(0, tk.END)
        for col in self.numeric_cols:
            if col != x_val and col != y_val:
                self.listbox.insert(tk.END, col)
                if col in selected_items:
                    self.listbox.selection_set(self.listbox.size() - 1)

    def generate_report(self):
        self.report_text.config(state="normal")
        self.report_text.delete("1.0", tk.END)
        
        x_val = self.comboX.get()
        y_val = self.comboY.get()
        
        covariates = [self.listbox.get(i) for i in self.listbox.curselection()]
        
        if x_val == y_val:
            self.report_text.insert(tk.END, "X and Y must be different")
            self.report_text.config(state="disabled")
            return
            
        res = PartialCorrelationCalculator.calculate(self.df, x_val, y_val, covariates)
        
        if 'error' in res:
            self.report_text.insert(tk.END, f"Error:\n{res['error']}")
        else:
            covar_str = ", ".join(covariates) if covariates else "None"
            
            report_str = f"Correlation between {x_val} and {y_val} without {covar_str} = {res['r']:.4f}\n"
            report_str += f"t-test = {res['t_stat']:.4f}\n"
            
            self.report_text.insert(tk.END, report_str)
            
        self.report_text.config(state="disabled")