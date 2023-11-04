import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from components.side_menu import SideMenu
from components.main_cointainer import MainContainer
from components.d_h_table import DHTable
from components.robot_arm import RobotArm
import json
import math
from tkinter import filedialog as fd

class App(ttk.Window):
    def __init__(self, theme, title, minsize):
        super().__init__(themename=theme, title=title, minsize=minsize)

        # Widgets
        self.side_menu = SideMenu(self, self.simulate_robot, self.save_robot, self.load_robot)
        self.d_h_table = DHTable(self, self.create_robot)

        # Layout
        self.side_menu.pack(side='left', fill='both', expand=False)
        self.side_menu.pack_propagate(0)

        self.d_h_table.pack(anchor='nw')
    

    def run(self):
        self.mainloop()
    
    def create_robot(self, dh_params):
        self.robot_arm = RobotArm(self, dh_params)
        self.robot_arm.show_robot()
    
    def save_robot(self):
        with open('test/my_robot_params.json', 'w') as params_file:
            json.dump(self.robot_arm.dh_params, params_file)
            params_file.close()

    def load_robot(self):
        open_file = fd.askopenfilename()
        with open(open_file, 'r') as params_file:
            robot_params = json.load(params_file)
        params_file.close()
        self.robot_arm = RobotArm(self, robot_params)
        self.robot_arm.robot.q = [0,math.pi/2,math.pi,-math.pi/2]
        self.robot_arm.show_robot()
        self.d_h_table.destroy()
        self.d_h_table = None
        self.main_container = MainContainer(self, name='main_frame', robot=self.robot_arm)
        self.main_container.pack(anchor='nw', expand=True, fill='both')

    def simulate_robot(self):
        print('Simulation!')

if __name__ == "__main__":
    app = App('darkly', 'Robot Arm Application', (1000,600))
    app.run()