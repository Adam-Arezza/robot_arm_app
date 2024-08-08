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