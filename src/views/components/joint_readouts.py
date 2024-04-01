#joint readout will show the angle value of a joint of the robot when in online mode

import ttkbootstrap as ttkb
from ttkbootstrap import IntVar

class JointReadout(ttkb.Frame):
    def __init__(self, parent, name):
        super().__init__(parent)
        self.joint_value = IntVar(value=0)
        self.value = ttkb.Label(self, textvariable=self.joint_value)
        self.joint_name = ttkb.Label(self, text=f'{name}')
        self.joint_name.pack(side='left')
        self.value.pack(side='left')


class ReadoutsFrame(ttkb.Frame):
    def __init__(self, parent, num_readouts):
        super().__init__(parent)
        self.readouts = []
        self.header = ttkb.Label(self,text='Joint Readouts')
        self.header.pack(anchor='nw')
        for i in range(num_readouts):
            readout = JointReadout(self, f'Joint {i}')
            readout.pack()
            self.readouts.append(readout)
