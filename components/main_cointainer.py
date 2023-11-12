import ttkbootstrap as ttk
from components.robot_config import RobotConfig
from components.table_header import TableHeader
from components.joint_config import JointConfig
from components.joint_meter import JointMeter
import math
from PIL import Image
Image.CUBIC = Image.BICUBIC

class MainContainer(ttk.Frame):
    def __init__(self, parent, name, robot_arm):
        super().__init__(parent, name=name, width=700)
        self.robot_arm = robot_arm
        self.headers = TableHeader(self, 
                                   name='robot_headers', 
                                   labels=['Theta (deg)', 'Alpha (deg)', 'r (m)', 'd (m)']
                                   )

        self.headers.pack()
        self.robot_config = RobotConfig(self, robot_arm.dh_params)
        self.robot_config.pack() 

        self.initial_joint_state = ttk.StringVar()
        self.previous_joint_state = ttk.StringVar()
        self.current_joint_state = ttk.StringVar()

        self.initial_joint_state.set(str(self.to_degrees(robot_arm.robot.q)))

        self.initial_joints = JointConfig(self, 'Initial Joint State',
                                          self.initial_joint_state)
        self.previous_joints = JointConfig(self, 'Previous Joint State',
                                           self.previous_joint_state)
        self.current_joints = JointConfig(self, 'Current Joint State',
                                           self.current_joint_state)
        
        self.initial_joints.pack(anchor='nw')
        self.previous_joints.pack(anchor='nw')
        self.current_joints.pack(anchor='nw')

        self.update_joint_btn = ttk.Button(self,
                                           text='Update joints', 
                                           command=self.update_joint_configs)
        self.update_joint_btn.pack(anchor='nw', pady=10, padx=10)


    def to_degrees(self, radians:list):
        result = []
        for i in radians:
            result.append(round(math.degrees(i)))

        return result

    def update_joint_configs(self):
       self.previous_joint_state.set(self.current_joint_state.get())
       self.current_joint_state.set(str(self.to_degrees(self.robot_arm.robot.q))) 
       