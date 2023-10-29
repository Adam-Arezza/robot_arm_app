import ttkbootstrap as ttk
import tkinter as tk

class TableRow(ttk.Frame):
    def __init__(self, parent, joint_name):
        super().__init__(parent)
        self.columns = []
        self.joint = joint_name
        self.params = [tk.StringVar(self, 0, f'{joint_name}_theta'), 
                       tk.StringVar(self, 0, f'{joint_name}_alpha'), 
                       tk.StringVar(self, 0, f'{joint_name}_r'), 
                       tk.StringVar(self, 0, f'{joint_name}_d')]
        self.label = ttk.Label(self, text=joint_name)
        for i in range(len(self.params)+1):
            col = None
            if i == 0:
                col = self.label
            else:
                col = ttk.Entry(self, textvariable=self.params[i-1])
            col.grid(row=0, column=i)
            self.columns.append(col)
            
