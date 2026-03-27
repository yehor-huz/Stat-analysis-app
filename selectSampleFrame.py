import tkinter as tk
from tkinter import scrolledtext
class SampleSelectionWidget(tk.Frame):
    def __init__(self, headers=[], master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=1)
        self.selectionList = headers
        self.textFrame = scrolledtext.ScrolledText(self, background='white')
        self.textFrame.config(state="disabled")
        self.textFrame.grid(column=0, row=0, sticky="NSEW")
        self.chekboxButtons = []
        self.update(headers)
        

    def update(self, selectionList):
        self.chekboxButtons.clear()
        self.textFrame.config(state="normal")
        self.textFrame.delete("1.0", tk.END)
        self.chekboxButtons.clear()
        self.selectionList = selectionList
        if len(self.selectionList) != 0:
            for header in self.selectionList:
                variable = tk.IntVar()
                self.chekboxButtons.append(variable)
                checkButton = tk.Checkbutton(self.textFrame, text=header, variable=variable)
                self.textFrame.window_create('end', window=checkButton)
                self.textFrame.insert('end', "\n")
        self.textFrame.config(state="disabled", cursor="")
        return
        
    def getSelection(self):
        selected_items = []
        for i, button in enumerate(self.chekboxButtons):
            if button.get() == 1:
                selected_items.append(self.selectionList[i])
        return selected_items
