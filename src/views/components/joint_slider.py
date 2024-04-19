import ttkbootstrap as ttkb
from ttkbootstrap.constants import GROOVE

class JointSlider(ttkb.Frame):
    def __init__(self, parent, joint_name, cb, joint_range):
        super().__init__(parent)
        self.slider_value = ttkb.IntVar()
        label = ttkb.Label(self, text=joint_name.replace("_", " ").capitalize())
        self.slider = ttkb.Scale(self, 
                          name=f'{joint_name}_slider', 
                          from_=joint_range[0], 
                          to=joint_range[1], 
                          value=0,
                          command=lambda s : self.set_slider_value(int(float(s))))
            
        value = ttkb.Label(parent, textvariable=self.slider_value, font='bold')
        label.pack(side='left', padx=10)
        self.slider.pack(side='left', padx=10, pady=10)
        value.pack()
        self.slider_cb = cb

    def set_slider_value(self, s:int):
        self.slider_value.set(s)
        self.slider_cb()


