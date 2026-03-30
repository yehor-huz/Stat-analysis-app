import tkinter as tk
from tkinter import scrolledtext
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure

from correlationCalculatorInterface import CorrelationCalculator


TYPE = ["Linear", "Non-Linear"]
METHOD = ["Pearson", "Spearman", "Kendall"]

class TypeWidget(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.calculator = CorrelationCalculator()
        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=1, weight=1)
        
        self.corrTypeFrame = scrolledtext.ScrolledText(self, background='white')
        self.corrTypeFrame.grid(column=0, row=0, sticky="NSEW")
        
        self.type = tk.StringVar(self, value=TYPE[0])
        
        self._build_radiobuttons(TYPE, self.corrTypeFrame, self.type)

        self.corrMethodFrame = scrolledtext.ScrolledText(self, background='white')
        self.corrMethodFrame.grid(column=0, row=1, sticky="NSEW")
        
        self.method = tk.StringVar(self, value=METHOD[0])
        
        self._build_radiobuttons(METHOD, self.corrMethodFrame, self.method)



    def _build_radiobuttons(self, type, frame, variable):
        frame.config(state="normal")
        
        frame.tag_configure("center", justify="center")
    
        for typeNames in type:
            rb = tk.Radiobutton(
                frame, 
                text=typeNames, 
                variable=variable, 
                value=typeNames, 
                indicatoron=0,           
                background="light gray", 
                selectcolor="gray",      
                width=15,                
                command=self.throwEvent  
            )
            
            frame.window_create("end", window=rb)
            frame.insert("end", "\n\n", "center")
            
        frame.config(state="disabled")

    def throwEvent(self):
        self.event_generate("<<TypeSelected>>")

    def getCorrMatrix(self, df):
            if df is None or df.empty:
                print("Дані відсутні!")
                return None
                
            current_type = self.type.get()
            current_method = self.method.get()

            if current_type == "Non-Linear":
                corr_matrix, sig_matrix = self.calculator.calculate_correlation_ratio(df)
                title = "Non linear (Correlation Ratio)"
                sig_name = "F"
                vmin, vmax = 0, 1 
            else:
                vmin, vmax = -1, 1 
                if current_method == "Pearson":
                    corr_matrix, sig_matrix = self.calculator.calculate_pearson(df)
                    title = "Pearson Correlation"
                    sig_name = "t"
                elif current_method == "Spearman":
                    corr_matrix, sig_matrix = self.calculator.calculate_spearman(df)
                    title = "Spearman Correlation"
                    sig_name = "t"
                elif current_method == "Kendall":
                    corr_matrix, sig_matrix = self.calculator.calculate_kendall(df)
                    title = "Kendall Correlation"
                    sig_name = "Z"

            annot_labels = np.empty_like(corr_matrix.values, dtype=object)
            
            for i in range(corr_matrix.shape[0]):
                for j in range(corr_matrix.shape[1]):
                    c_val = corr_matrix.iloc[i, j]
                    s_val = sig_matrix.iloc[i, j]
                    
                    if pd.isna(s_val):
                        s_str = "NaN"
                    elif np.isinf(s_val):
                        s_str = "inf"
                    else:
                        s_str = f"{s_val:.2f}"
                    
                    annot_labels[i, j] = f"{c_val:.2f}\n({sig_name}: {s_str})"

            fig = Figure(figsize=(6, 5), dpi=100)
            ax = fig.add_subplot(111)

            sns.heatmap(
                corr_matrix.astype(float), 
                annot=annot_labels,  
                fmt="",              
                cmap="coolwarm",   
                vmin=vmin,         
                vmax=vmax,         
                ax=ax,
                cbar_kws={'label': 'Correlation coef.'}
            )
            
            ax.set_title(title, pad=15)
            fig.tight_layout() 

            return fig


    