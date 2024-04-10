import ttkbootstrap as ttkb
import tkinter as tk
from ttkbootstrap.constants import GROOVE

class TableRow(ttkb.Frame):
    def __init__(self, parent, cols, name='', header=False, values=[]):
        super().__init__(parent)
        self.columns = []
        self.name = name
        self.params = [ttkb.StringVar(self, value=0) for i in range(cols)]
        self.header = header
        for i in range(cols):
            col = None
            if self.header:
                col = ttkb.Label(self, text=f"{values[i]}", width=16)
                col.configure(anchor='nw', borderwidth=1, relief=GROOVE, padding=(5,5))
            else:
                col = ttkb.Entry(self, textvariable=self.params[i], width=16)
            col.grid(row=0, column=i)
            self.columns.append(col)
