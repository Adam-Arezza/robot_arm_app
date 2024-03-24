import roboticstoolbox as rtb
from ttkbootstrap.dialogs.dialogs import Messagebox
from src.views.components.side_menu import SideMenu

class SideMenuController:
    def __init__(self, root, parent):
        self.root = root
        self.view = SideMenu(parent, {}, self)
        self.parent = parent
    def show_view(self):
        self.view.configure(width=self.parent.winfo_width() * 0.2)
        self.view.pack_propagate(0)
        self.view.pack(side='left', expand=False, fill='both', padx=0, anchor='w')


    def kill_view(self):
        print("Closing the side menu.")
        self.view.destroy()

    def save_robot(self):
        #Add joint limits into the saved file
        save_file = fd.askopenfilename()
        with open(save_file,'w') as params_file:
            json.dump(self.root.robot_arm.dh_params, params_file)
            params_file.close()

    def teach_pendant(self):
        self.root.teach_pendant()

    def show_robot(self):
        self.root.show_robot()

    def load_robot(self):
        self.root.load_robot()

    def reset_robot(self):
        self.root.reset_robot()

    def create_robot(self):
        self.root.create_robot()

    def toggle_auto_manual(self):
        self.root.mode = not self.root.mode
