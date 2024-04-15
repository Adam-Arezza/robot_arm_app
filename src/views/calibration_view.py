import ttkbootstrap as ttkb
from src.views.components.joint_readouts import ReadoutsFrame
from src.views.components.button_group import ButtonGroup

class CalibrationView(ttkb.Frame):
    def __init__(self,parent,joints):
        super().__init__(parent)
        self.header = ttkb.Label(self, text='Calibration', font=('default', 12,'bold'))
        self.header.pack()
        self.calibration_btns = ButtonGroup(self,
                                            [('Start',),
                                             ('Stop',),
                                             ('Set',)],
                                            horizontal=True,
                                            style='primary.TButton',
                                            container_style='default'
                                            )


        self.readouts = ReadoutsFrame(self,len(joints))
        self.calibration_btns.pack()
        self.readouts.pack()
