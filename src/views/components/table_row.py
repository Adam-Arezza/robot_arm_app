import ttkbootstrap as ttkb
import tkinter as tk

class TableRow(ttkb.Frame):
    def __init__(self, parent, joint_name, num_joints):
        super().__init__(parent)
        self.columns = []
        self.joint = joint_name
        self.params = [ttkb.StringVar(self, value=0) for i in range(num_joints)]
        #self.params = [tk.StringVar(self, 0, f'{joint_name}_theta'), 
        #               tk.StringVar(self, 0, f'{joint_name}_alpha'), 
        #               tk.StringVar(self, 0, f'{joint_name}_r'), 
        #               tk.StringVar(self, 0, f'{joint_name}_d')]
        self.label = ttkb.Label(self, text=joint_name)
        
        for i in range(num_joints+1):
            col = None
            if i == 0:
                col = self.label
            else:
                col = ttkb.Entry(self, textvariable=self.params[i-1])
            col.grid(row=0, column=i)
            self.columns.append(col)
