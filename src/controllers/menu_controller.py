import roboticstoolbox as rtb
import ttkbootstrap as ttkb
import json
from ttkbootstrap.dialogs.dialogs import Messagebox
from tkinter import filedialog as fd
from src.views.d_h_table import DHTable


class MenuController:
    def __init__(self, root):
        self.root = root
        

    def save_robot(self):
        #Add joint limits into the saved file
        save_file = fd.asksaveasfilename(defaultextension='json')
        with open(save_file,'w') as params_file:
            json.dump(self.root.robot_controller.model.dh_params, params_file)
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
        self.dh_window = ttkb.window.Toplevel(self.root)
        self.dh_table = DHTable(self.dh_window, self.root.create_robot)
        self.dh_table.pack()


    def show_help_dialog(self):
        pass


    def exit(self):
        self.root.on_close()

