import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *

class JointConfigurationTable(ttk.Frame):
    def __init__(self, parent, initial_joint_config):
        super().__init__(parent)

        self.headers = [f'Joint{i}' for i in range(len(initial_joint_config))]
        self.joint_table = Tableview(
            self,
            coldata=self.headers,
            rowdata=[initial_joint_config],
            height=10,
            bootstyle='light' 
        )
        self.joint_table.pack()