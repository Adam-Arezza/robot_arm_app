import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from components.side_menu import SideMenu
from components.main_cointainer import MainContainer
from components.d_h_table import DHTable
from components.robot_arm import RobotArm
import json
from tkinter import filedialog as fd
from components.button_group import ButtonGroup
import math

class App(ttk.Window):
    def __init__(self, theme, title, minsize):
        super().__init__(themename=theme, title=title, minsize=minsize)

        self.initial_btns = ButtonGroup(self,
                                        buttons=[('Create DH robot', self.create_dh_robot),
                                                 ('Load robot', self.load_robot)])
        self.initial_btns.pack(pady=minsize[1] / 2)
         

    def create_robot(self, dh_params):
        self.robot_arm = RobotArm(self,
                                  dh_params,
                                  initial_joint_states = [0,math.pi/2,math.pi,-math.pi/2])

        self.robot_arm.show_robot()
        self.d_h_table.destroy()
        self.d_h_table = None
        self.create_side_menu()
        self.main_container = MainContainer(self, name='main_frame', robot=self.robot_arm)
        self.main_container.pack(anchor='nw', expand=True, fill='both')

    def create_dh_robot(self):
        self.initial_btns.destroy()
        self.d_h_table = DHTable(self, self.create_robot)
        self.d_h_table.pack()

    def save_robot(self):
        save_file = fd.askopenfilename()
        with open(save_file,'w') as params_file:
            json.dump(self.robot_arm.dh_params, params_file)
            params_file.close()

    def load_robot(self):
        self.initial_btns.destroy()
        open_file = fd.askopenfilename()
        with open(open_file, 'r') as params_file:
            robot_params = json.load(params_file)
        params_file.close()
        self.create_side_menu()
        self.robot_arm = RobotArm(self, 
                                  robot_params,
                                  initial_joint_states = [0,math.pi/2,math.pi,-math.pi/2])
        self.robot_arm.show_robot()
        self.main_container = MainContainer(
            self, name='main_frame', robot_arm=self.robot_arm)
        self.main_container.pack(expand=True, fill='both')

    def teach_pendant(self):
        self.robot_arm.robot.teach(self.robot_arm.robot.q)

    def show_robot(self):
        self.robot_arm.robot.plot(self.robot_arm.robot.q)
    
    def create_side_menu(self):
        self.side_menu = SideMenu(self,
                                  self.save_robot,
                                  self.teach_pendant,
                                  self.show_robot)
        self.side_menu.pack(side='left', fill='y')
    
if __name__ == "__main__":
    app = App('cyborg', 'Robot Arm Application', (800, 600))
    app.mainloop()
