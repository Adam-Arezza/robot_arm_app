import roboticstoolbox as rtb
import ttkbootstrap as ttkb
import json
from ttkbootstrap.dialogs.dialogs import Messagebox
from tkinter import filedialog as fd
from src.views.d_h_table import DHTable
from src.views.components.menu import Menu
from src.views.calibration_view import CalibrationView
from src.views.pose_generator_view import PoseGenerator
from src.handlers.pose_generator_handler import PoseGeneratorHandler


class MenuHandler:
    def __init__(self, root):
        self.root = root
        self.view = Menu(root, {}, self)
        self.calibration_window = None
        self.pose_generator_window = None
        self.dh_window = None


    def save_robot(self):
        #Add joint limits into the saved file
        save_file = fd.asksaveasfilename(defaultextension='json')
        with open(save_file,'w') as params_file:
            json.dump(self.root.main_container.robot_handler.model.dh_params, params_file)
            params_file.close()


    def load_robot(self):
        open_file = fd.askopenfilename()
        with open(open_file, 'r') as params_file:
            params = json.load(params_file)
        params_file.close()
        self.root.create_robot(params)


    def reset_robot(self):
        self.root.reset_robot()


    def create_robot(self):
        if not self.dh_window:
            self.dh_window = ttkb.window.Toplevel(self.root)
            self.dh_table = DHTable(self.dh_window, self.root.create_robot)
            self.dh_table.pack()


    def show_help_dialog(self):
        pass


    def open_calibration(self):
        if not self.calibration_window:
            self.calibration_window = ttkb.window.Toplevel(self.root)
            self.calibration_view = CalibrationView(self.calibration_window, self.root.main_container.robot_handler.model.robot.links)
            self.calibration_view.pack()
        else:
            return


    def open_pose_generator(self):
        if not self.pose_generator_window:
            self.pose_generator_window = ttkb.window.Toplevel(self.root)
            pose_generator_view = PoseGenerator(self.pose_generator_window)
            pose_generator_handler = PoseGeneratorHandler(pose_generator_view, self.root.robot_model)
            pose_generator_view.pack(padx=30, pady=30)
        else:
            return


    def exit(self):
        self.root.on_close()

