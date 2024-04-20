import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from src.views.main_cointainer import MainContainer
from src.models.robot_model import RobotArm
from src.controllers.robot_controller import RobotController
from src.views.robot_view import RobotView


class App(ttkb.Window):
    def __init__(self, theme, title, minsize, maxsize):
        super().__init__(themename=theme, 
                         title=title,
                         minsize=minsize,
                         maxsize=maxsize)
        self.maxsize = (self.winfo_screenwidth(),self.winfo_screenheight())
        self.resizable(True,True)
        self.main_container = MainContainer(self)
        self.main_container.pack(padx=0, pady=0, fill='both', expand=True)
        self.main_container.columnconfigure(0, weight=1)
        self.main_container.rowconfigure(1, weight=1)
        self.simulation_mode = True


    def create_robot(self, dh_params:dict):
        robot_model = RobotArm(dh_params, mode=False)
        self.main_container.robot_controller.add_model(robot_model)
        self.main_container.main_view()


    def show_configuration(self, cfg:list):
        self.main_container.robot_controller.show_joint_config(cfg)


    def simulate_trajectory(self, trajectory:list):
        self.main_container.robot_controller.simulate_trajectory(trajectory)


    def set_sim_mode(self, mode:bool):
        self.simulation_mode = mode


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
    app = App('flatly', 'Robot Arm Application',(960,720),(1440,960))
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()

