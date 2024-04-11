import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from src.views.main_cointainer import MainContainer
from src.models.robot_model import RobotArm
from src.controllers.robot_controller import RobotController
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
        self.main_container.columnconfigure(0, weight=1)
        self.main_container.rowconfigure(1, weight=1)


    def create_robot(self, dh_params):
        robot_model = RobotArm(dh_params, mode=False)
        self.main_container.robot_controller.add_model(robot_model)
        self.main_container.main_view()


    def show_configuration(self, cfg):
        self.main_container.robot_controller.show_joint_config(cfg)


    def show_trajectory(self, trajectory):
        self.main_container.robot_controller.show_trajectory(trajectory)


    def reset_robot(self):
        self.main_container.robot_controller.reset()


    def on_close(self):
        try:
            self.main_container.on_close()
            self.destroy()
        except Exception as e:
            print(e)
            self.destroy()

if __name__ == "__main__":
    app = App('flatly', 'Robot Arm Application')
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()

