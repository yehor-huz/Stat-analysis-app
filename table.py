import tkinter as tk
from tkinter import scrolledtext
import pandas as pd
import numpy as np
import scipy.stats as stats
import seaborn as sns
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ContingencyCalculator:
    @staticmethod
    def calculate(series_x: pd.Series, series_y: pd.Series) -> dict:
        df_clean = pd.concat([series_x, series_y], axis=1).dropna()
        x_clean = df_clean.iloc[:, 0]
        y_clean = df_clean.iloc[:, 1]
        
        contingency_table = pd.crosstab(x_clean, y_clean)
        n = contingency_table.values.sum()
        
        chi2, p_val, dof, expected = stats.chi2_contingency(contingency_table)
        
        pearson_c = np.sqrt(chi2 / (n + chi2))
        
        phi = None
        if contingency_table.shape == (2, 2):
            N00 = contingency_table.iloc[0, 0]
            N01 = contingency_table.iloc[0, 1]
            N10 = contingency_table.iloc[1, 0]
            N11 = contingency_table.iloc[1, 1]
            
            N0 = N00 + N01
            N1 = N10 + N11
            M0 = N00 + N10
            M1 = N01 + N11
            
            denom = np.sqrt(N0 * N1 * M0 * M1)
            if denom != 0:
                phi = (N00 * N11 - N01 * N10) / denom
            else:
                phi = 0.0

        return {
            'table': contingency_table,
            'n': n,
            'chi2': chi2,
            'p_value': p_val,
            'dof': dof,
            'pearson_c': pearson_c,
            'phi': phi
        }


class ContingencyVisualizer:
    
    @staticmethod
    def get_heatmap(crosstab_df: pd.DataFrame, xlabel: str, ylabel: str) -> Figure:
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        sns.heatmap(
            crosstab_df, 
            annot=True,     
            fmt="d",        
            cmap="YlGnBu",  
            cbar_kws={'label': 'Absolute frequence'},
            ax=ax
        )
        ax.set_xlabel(xlabel, fontweight='bold', labelpad=10)
        ax.set_ylabel(ylabel, fontweight='bold', labelpad=10)
        ax.set_title("Conjuction table", pad=15)
        
        fig.tight_layout()
        return fig


class ContingencyAnalysisWindow(tk.Toplevel):
    
    def __init__(self, df: pd.DataFrame, col_x: str, col_y: str, master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.geometry("900x500")
        self.minsize(800, 450)
        
        self.columnconfigure(index=0, weight=3)
        self.columnconfigure(index=1, weight=2)
        self.rowconfigure(index=0, weight=1)
        
        self.plot_frame = tk.Frame(self, bg="white", bd=1, relief=tk.SUNKEN)
        self.plot_frame.grid(row=0, column=0, sticky="NSEW", padx=10, pady=10)
        
        self.report_text = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.report_text.grid(row=0, column=1, sticky="NSEW", padx=10, pady=10)
        
        self._generate_analysis(df, col_x, col_y)

    def _generate_analysis(self, df: pd.DataFrame, col_x: str, col_y: str):
        results = ContingencyCalculator.calculate(df[col_x], df[col_y])
        
        fig = ContingencyVisualizer.get_heatmap(results['table'], col_x, col_y)
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self._build_report(results, col_x, col_y)

    def _build_report(self, res: dict, col_x: str, col_y: str):
        self.report_text.config(state="normal")
        self.report_text.delete("1.0", tk.END)
        
        report = []
        report.append("="*40)
        report.append(f"Feature X: {col_y}")
        report.append(f"Feature Y: {col_x}")

        report.append(f"χ2: {res['chi2']:.4f}")
        
        p_val = res['p_value']
        p_str = f"{p_val:.4e}" if p_val < 0.0001 else f"{p_val:.4f}"
        report.append(f"p-value: {p_str}")
        
        if p_val < 0.05:
            report.append("Features are connected.\n")
        else:
            report.append("Features are independent.\n")
            
        report.append(f"Pearson Coeficient (C): {res['pearson_c']:.4f}")
        
        if res['phi'] is not None:
            report.append(f"Ф Coeficient: {res['phi']:.4f}")
            
        report.append("="*40)
        
        self.report_text.insert(tk.END, "\n".join(report))
        self.report_text.config(state="disabled")