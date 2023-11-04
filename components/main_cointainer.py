import ttkbootstrap as ttk
from components.robot_config import RobotConfig
from components.table_header import TableHeader
from components.joint_slider import JointSlider

class MainContainer(ttk.Frame):
    def __init__(self, parent, name, robot):
        super().__init__(parent, name=name)
        self.headers = TableHeader(self, name='robot_headers', labels=['Theta (deg)', 'Alpha (deg)', 'r (m)', 'd (m)'])
        self.headers.pack(anchor='nw')
        self.robot_config = RobotConfig(self, robot.dh_params)
        self.sliders = []

        for i in range(4):
            slider = JointSlider(self, joint_name=f'joint_{i}')
            slider.pack(anchor='nw', padx=10, pady=15)
            self.sliders.append(slider)