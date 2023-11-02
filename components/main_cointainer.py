import ttkbootstrap as ttk
from components.robot_config import RobotConfig
from components.table_header import TableHeader

class MainContainer:
    def __init__(self, parent, robot):
        self.parent = parent
        self.frame = ttk.Frame(self.parent, name='main_frame')
        self.frame.pack(anchor='nw', expand=True, fill='both')
        self.frame.pack_propagate(0)
        self.headers = TableHeader(self.frame, 'g')
        self.robot_config = RobotConfig(self.frame, robot.dh_params)
