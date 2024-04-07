from src.views.start_view import StartView
from src.views.d_h_table import DHTable
from tkinter import filedialog as fd
import json
from src.utils import find

class StartViewController:
    def __init__(self, root, parent):
        self.root = root
        self.view = StartView(parent)
        self.parent = parent
        create_robot_btn = self.view.initial_btns.buttons["create_dh_robot"]
        create_robot_btn.configure(command=self.create_dh_robot)
        load_btn = self.view.initial_btns.buttons["load_robot"]
        load_btn.configure(command=self.load_robot)

    def load_robot(self):
        open_file = fd.askopenfilename()
        with open(open_file, 'r') as params_file:
            params = json.load(params_file)
        params_file.close()
        self.root.create_robot(params)
        self.view.destroy()


    def create_dh_robot(self):
        self.view.destroy()
        self.view = DHTable(self.parent, self.create_robot)
        self.show_view()


    def create_robot(self, params):
        self.view.destroy()
        self.root.create_robot(params)


    def show_view(self):
        self.view.pack(expand=True, fill='both')


    def kill_view(self):
        self.view.destroy()

