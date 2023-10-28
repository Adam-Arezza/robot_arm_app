import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from components.side_menu import SideMenu
from components.main_canvas import MainCanvas

class App:
    def __init__(self, root):
        self.root = root
        self.root.resizable(False,False)
        self.side_menu = SideMenu(root)
        self.main_canvas = MainCanvas(root)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App(ttk.Window(themename="darkly", size=(1200,1000), title='Robot Arm Application'))
    app.run()