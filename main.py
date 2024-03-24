import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from src.views.start import StartView
from src.views.main_cointainer import MainContainer
from src.models.robot_model import RobotArm
from src.controllers.robot_controller import RobotController
from src.controllers.start_view_controller import StartViewController
import math
from src.views.robot_view import RobotView


class App(ttkb.Window):
    def __init__(self, theme, title):
        super().__init__(themename=theme, 
                         title=title,
                         minsize=(960,720))
        self.maxsize = (self.winfo_screenwidth(),self.winfo_screenheight())
        self.resizable(True,True)
        self.main_container = MainContainer(self)
        self.main_container.pack(padx=0, pady=0, fill='both', expand=True)

        self.mode = 'manual'

    def create_robot(self, dh_params):
        self.robot_controller = RobotController(RobotView(self, self.main_container), RobotArm(dh_params))
        self.main_container.main_view()


    def show_configuration(self, cfg):
        self.robot_controller.show_joint_config(cfg)


    def show_trajectory(self, trajectory):
        self.robot_controller.show_trajectory(trajectory)

    def reset_robot(self):
        self.robot_controller.reset()

    def show_robot(self):
        self.robot_controller.show_robot()

    def teach_pendant(self):
        self.robot_controller.teach_pendant()

    
    def on_close(self):
        try:
            self.main_container.on_close()
            self.destroy()
        except Exception as e:
            self.destroy()

if __name__ == "__main__":
    app = App('flatly', 'Robot Arm Application')
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()

