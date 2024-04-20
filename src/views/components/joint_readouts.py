import ttkbootstrap as ttkb
from ttkbootstrap import IntVar
from ttkbootstrap.constants import GROOVE


class JointReadout(ttkb.Frame):
    def __init__(self, parent, name):
        super().__init__(parent)
        self.joint_value = IntVar(value=0)
        self.value = ttkb.Label(self, 
                                textvariable=self.joint_value, 
                                borderwidth=1, 
                                width=8, 
                                relief=GROOVE,
                                font=('default',10, 'bold'),
                                background='#b5c7f8')
        self.joint_name = ttkb.Label(self, 
                                     text=f'{name}',
                                     font=('default',10,'bold'))
        self.joint_name.pack(side='left')
        self.value.pack(side='left')


class ReadoutsFrame(ttkb.Frame):
    def __init__(self, parent, num_readouts):
        super().__init__(parent)
        self.readouts = []
        self.header = ttkb.Label(self,
                                 text='Joint Angles',
                                 font=('default',12, 'bold'))
        self.header.pack(anchor='nw',pady=5)
        for i in range(num_readouts):
            readout = JointReadout(self, f'Joint {i+1}')
            readout.pack(fill='x', expand=True)
            self.readouts.append(readout)
