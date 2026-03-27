import tkinter as tk
from tkinter import messagebox, ttk
from scipy import special, stats
import numpy as np

TRANSFORMATIONS = ["None", "log", "Box-Cox", "Yeo-Johnson"]

class TransformerWidget(tk.Frame):
    def __init__(self, sample, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.sample = dict.fromkeys(TRANSFORMATIONS, None)
        self.currentTransformation = TRANSFORMATIONS[0]
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.transformer = ttk.Combobox(self, values=TRANSFORMATIONS, state="readonly")
        self.transformer.set(TRANSFORMATIONS[0])
        self.sample[TRANSFORMATIONS[0]] = sample
        self.transformer.bind("<<ComboboxSelected>>", self.transform)
        
        self.transformer.grid(row=0, column=0, padx=20, pady=20)

    def transform(self, event):
            selectedTransformation = TRANSFORMATIONS[self.transformer.current()]
            original = self.sample[TRANSFORMATIONS[0]]

            if self.sample[selectedTransformation] is None:
                newDataFrame = original.copy()
                numericColumns = newDataFrame.select_dtypes(include=np.number).columns
                if selectedTransformation == TRANSFORMATIONS[1]: 
                    newDataFrame[numericColumns] = np.log1p(newDataFrame[numericColumns])
                    
                elif selectedTransformation == TRANSFORMATIONS[2]: 
                    for col in numericColumns:
                        if (newDataFrame[col].dropna() > 0).all():
                            newDataFrame[col], _ = stats.boxcox(newDataFrame[col].dropna())
                        else:
                            print(f"Skipped column {col} (non-numeric values)")
                            
                elif selectedTransformation == TRANSFORMATIONS[3]: 
                    for col in numericColumns:
                        newDataFrame[col], _ = stats.yeojohnson(newDataFrame[col].dropna())
                
                self.sample[selectedTransformation] = newDataFrame
                
            self.currentTransformation = selectedTransformation
            print(self.sample[selectedTransformation])
            self.event_generate("<<DataTransformed>>")
            
    
    def update(self, sample):
        self.sample = dict.fromkeys(TRANSFORMATIONS, None)
        self.transformer.set(TRANSFORMATIONS[0])
        self.sample[TRANSFORMATIONS[0]] = sample

    def get(self):
        return self.sample[self.currentTransformation]

