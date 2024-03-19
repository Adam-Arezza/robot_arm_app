import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview


class RobotConfig(ttk.Frame):
    def __init__(self, parent, robot_config, headers):
        super().__init__(parent)
 
        self.robot_config = robot_config
        self.font = ttk.font.Font(size=12)
        self.rows = []

        self.col_data = headers 
        self.row_data = robot_config.values()
        self.table = Tableview(self,
                               coldata=self.col_data,
                               rowdata=self.row_data,
                               autofit=True,
                               height=6)
        self.table.pack(side='left')

