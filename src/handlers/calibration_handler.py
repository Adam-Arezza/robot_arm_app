import spatialmath as sm
from src.views.calibration_view import CalibrationView

class CalibrationHandler:
    def __init__(self, parent, robot_model):
        self.view = CalibrationView(parent)
        self.robot_model = robot_model
        self.view.calibration_btns.buttons['set'].configure(command=self.set_offset)
        self.view.pack()
    

    def set_offset(self):
        offset = float(self.view.offset.get())
        self.robot_model.robot.links[-1].a += offset
        self.robot_model.ee_offset = offset
       # tool_offset = sm.SE3(offset, 0, 0)
       # self.robot_model.robot.tool = tool_offset

        #try recreating the robot model
        #ee_link = list(self.robot_model.dh_params.keys())[-1]
        #self.robot_model.dh_params[f"{ee_link}"][2] = float(self.robot_model.dh_params[f"{ee_link}"][2])+ offset

