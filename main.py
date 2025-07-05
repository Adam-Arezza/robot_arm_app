import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from src.views.main_cointainer import MainContainer
from src.robot_model import RobotArm
#from src.handlers.robot_handler import RobotHandler
from src.views.robot_view import RobotView
from src.views.styles import create_style_set


class App(ttkb.Window):
    def __init__(self, theme, title:str):
        super().__init__(themename=theme, title=title)
        self.robot_model = None
        self.maxsize = (self.winfo_screenwidth(),self.winfo_screenheight())
        self.resizable(True,True)
        self.geometry(f"{int(self.maxsize[0]/2)}x{int(self.maxsize[1]/2)}")
        create_style_set()
        self.main_container = MainContainer(self)
        self.main_container.pack(padx=0, pady=0, fill='both', expand=True)
        self.online_mode = False


    def create_robot(self, dh_params:dict):
        #TODO create input for initial joint states in dh table
        self.robot_model = RobotArm(dh_params, mode=False, initial_joint_states=[0, 90, 0, 0])
        self.main_container.main_view(self.robot_model)


    def show_configuration(self, cfg:list):
        self.main_container.robot_handler.show_joint_config(cfg)


    def simulate_trajectory(self, trajectory:list):
        self.main_container.robot_handler.simulate_trajectory(trajectory)


    def set_online_mode(self, mode:bool):
        self.online_mode = mode


    def update_robot_state(self):
        self.main_container.robot_handler.update_joint_positions()


    def on_close(self):
        try:
            self.main_container.destroy()
            exit(0)
        except Exception as e:
            print(e)
            exit(0)

if __name__ == "__main__":
    app = App('flatly', 'Robot Arm Application')
    app.state("zoomed")
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()

