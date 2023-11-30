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
from PIL import Image, ImageTk


class App(ttk.Window):
    def __init__(self, theme, title, minsize):
        super().__init__(themename=theme, title=title, minsize=minsize)

        self.image = Image.open('assets/robot.png')
        width = self.image.width
        height = self.image.height
        self.robot_img = self.image.resize((int(width/3), int(height/3)))
        self.robot_image = ImageTk.PhotoImage(self.robot_img)
        self.image_label = ttk.Label(self,image=self.robot_image)
        self.image_label.pack(pady=(100,0))

        self.initial_btns = ButtonGroup(self,
                                        buttons=[('Create DH robot', self.create_dh_robot),
                                                 ('Load robot', self.load_robot)],
                                        container_style='default')
        self.initial_btns.pack(pady=30)


    def create_robot(self, dh_params):
        self.robot_arm = RobotArm(self,
                                  dh_params,
                                  initial_joint_states = [0,math.pi/2,math.pi,-math.pi/2])
 
        self.d_h_table.pack_forget()
        self.main_container = MainContainer(self, name='main_frame', robot_arm=self.robot_arm)
        self.create_side_menu()
        self.main_container.pack(anchor='nw', expand=True, fill='both')
        self.robot_arm.show_robot()

    def create_dh_robot(self):
        self.image_label.destroy()
        self.initial_btns.destroy()
        self.d_h_table = DHTable(self, self.create_robot)
        self.d_h_table.pack()

    def save_robot(self):
        #Add joint limits into the saved file
        save_file = fd.askopenfilename()
        with open(save_file,'w') as params_file:
            json.dump(self.robot_arm.dh_params, params_file)
            params_file.close()

    def load_robot(self):
        self.image_label.destroy()
        self.initial_btns.destroy()
        open_file = fd.askopenfilename()
        with open(open_file, 'r') as params_file:
            robot_params = json.load(params_file)
        params_file.close()
        self.robot_arm = RobotArm(self, 
                                  robot_params,
                                  initial_joint_states = [0,math.pi/2,math.pi,-math.pi/2])
        self.main_container = MainContainer(self, name='main_frame', robot_arm=self.robot_arm)

        self.create_side_menu() 
        self.main_container.pack(expand=True, fill='both')
        self.robot_arm.show_robot()

    def teach_pendant(self):
        self.robot_arm.robot.teach(self.robot_arm.robot.q)
        #self.main_container.robot_view._add_teach_panel(self.robot_arm.robot, self.robot_arm.robot.q)

    def show_robot(self):
        self.robot_arm.robot.plot(self.robot_arm.robot.q)

    def create_side_menu(self):
        self.side_menu = SideMenu(self,
                                  self.save_robot,
                                  self.teach_pendant,
                                  self.show_robot)
        self.side_menu.pack(side='left', fill='y')

    def on_close(self):
        try:
            if self.main_container:
                if self.main_container.serial_connector:
                    self.main_container.serial_connector.on_close()
            self.destroy()
        except Exception as e:
            self.destroy()

if __name__ == "__main__":
    app = App('journal', 'Robot Arm Application', (800, 600))
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
