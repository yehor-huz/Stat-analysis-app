import tkinter as tk
from tkinter import ttk, scrolledtext
import numpy as np
import pandas as pd
from multipleCorrelationCalculator import MultipleCorrelationCalculator

class MultipleCorrelationWindow(tk.Toplevel):
    def __init__(self, df: pd.DataFrame, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.df = df
        self.numeric_cols = self.df.select_dtypes(include=np.number).columns.tolist()
        
        self.title("MultipleCorrelation")
        self.geometry("800x400")
        self.minsize(700, 350)
        
        self.columnconfigure(0, weight=1, uniform="col")
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        
        self._build_ui()
        self._populate_listbox()
        self.generate_report()

    def _build_ui(self):
        frame_target = tk.Frame(self)
        frame_target.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="EW")
        tk.Label(frame_target, text="Feature:").pack(anchor="w")
        
        self.combo_target = ttk.Combobox(frame_target, values=self.numeric_cols, state="readonly")
        if len(self.numeric_cols) > 0: self.combo_target.current(0)
        self.combo_target.pack(fill="x")
        self.combo_target.bind("<<ComboboxSelected>>", self._on_combobox_change)

        frame_preds = tk.Frame(self)
        frame_preds.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="NSEW")
        
        tk.Label(frame_preds, text="Other features:").pack(anchor="w")
        
        scroll_y = tk.Scrollbar(frame_preds)
        scroll_y.pack(side="right", fill="y")
        
        self.listbox = tk.Listbox(frame_preds, selectmode=tk.MULTIPLE, yscrollcommand=scroll_y.set)
        self.listbox.pack(side="left", fill="both", expand=True)
        scroll_y.config(command=self.listbox.yview)
        
        self.listbox.bind("<<ListboxSelect>>", lambda e: self.generate_report())

        self.report_text = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.report_text.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="NSEW")

    def _on_combobox_change(self, event):
        self._populate_listbox()
        self.generate_report()

    def _populate_listbox(self):
        target_val = self.combo_target.get()
        selected_items = [self.listbox.get(i) for i in self.listbox.curselection()]
        
        self.listbox.delete(0, tk.END)
        for col in self.numeric_cols:
            if col != target_val:
                self.listbox.insert(tk.END, col)
                if col in selected_items:
                    self.listbox.selection_set(self.listbox.size() - 1)

    def generate_report(self):
        self.report_text.config(state="normal")
        self.report_text.delete("1.0", tk.END)
        
        target_val = self.combo_target.get()
        predictors = [self.listbox.get(i) for i in self.listbox.curselection()]
        
        if not predictors:
            self.report_text.insert(tk.END, "Choose at least one predictor feature.")
            self.report_text.config(state="disabled")
            return
            
        res = MultipleCorrelationCalculator.calculate(self.df, target_val, predictors)
        
        if 'error' in res:
            self.report_text.insert(tk.END, f"Error: \n{res['error']}")
        else:
            preds_str = ", ".join(predictors)
            
            report_str = f"Multiple Correlation between [{target_val}] and [{preds_str}]:\n\n"
            report_str += f"R  = {res['r_mult']:.4f}\n"
            report_str += f"R² = {res['r_squared']:.4f}\n\n"
            
            report_str += f"F-test = {res['f_stat']:.4f}\n"

            
            self.report_text.insert(tk.END, report_str)
            
        self.report_text.config(state="disabled")