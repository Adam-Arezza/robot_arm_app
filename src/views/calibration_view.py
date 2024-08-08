import ttkbootstrap as ttkb
from src.views.components.button_group import ButtonGroup


class CalibrationView(ttkb.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.header = ttkb.Label(self, text='Calibration', font=('default', 12,'bold'))
        self.header.pack()
        self.offset = ttkb.StringVar(value=0)
        self.calibration_btns = ButtonGroup(self,
                                            [('Set',)],
                                            horizontal=True,
                                            style='secondary.TButton',
                                            container_style='default'
                                            )
        self.offset_entry = ttkb.Entry(self, textvariable=self.offset)
        self.offset_entry.pack()
        self.calibration_btns.pack()
