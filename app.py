import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from components.side_menu import SideMenu
from components.main_cointainer import MainContainer
from components.d_h_table import DHTable
from components.robot_arm import RobotArm
import json
import math

class App:
    def __init__(self, root):
        self.root = root
        # self.root.resizable(False,False)
        self.side_menu = SideMenu(root, self.simulate_robot, self.save_robot, self.load_robot)
        self.d_h_table = DHTable(root, self.create_robot)
        self.main_container = MainContainer(root)
    
    def run(self):
        self.root.mainloop()
    
    def create_robot(self, dh_params):
        self.robot_arm = RobotArm(self.root, dh_params)
        self.robot_arm.show_robot()
    
    def save_robot(self):
        with open('test/my_robot_params.json', 'w') as params_file:
            json.dump(self.robot_arm.dh_params, params_file)
            params_file.close()

    def load_robot(self):
        with open('test/my_robot_params.json', 'r') as params_file:
            robot_params = json.load(params_file)
        self.robot_arm = RobotArm(self.root, robot_params)
        self.robot_arm.robot.q = [0,math.pi/2,math.pi,-math.pi/2]
        self.robot_arm.show_robot()

    def simulate_robot(self):
        print('Simulation!')

if __name__ == "__main__":
    app = App(ttk.Window(themename="darkly", title='Robot Arm Application', size=(1200, 900)))
    app.run()