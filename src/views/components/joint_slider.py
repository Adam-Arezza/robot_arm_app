import ttkbootstrap as ttkb
from ttkbootstrap.constants import GROOVE

class JointSlider(ttkb.Frame):
    def __init__(self, parent, joint_name, cb, joint_range, default_value, slider_idx):
        super().__init__(parent)
        #self.configure(borderwidth=1, relief=GROOVE)
        self.slider_value = ttkb.IntVar()
        label = ttkb.Label(self, text=joint_name.replace("_", " ").capitalize(), font=('Helvetica', 10, 'bold'))
        self.size = 200
        self.slider_idx = slider_idx
        self.slider = ttkb.Scale(self, 
                          name=f'{joint_name}_slider', 
                          from_=joint_range[0], 
                          to=joint_range[1], 
                          value=default_value,
                          length=self.size,
                          command=lambda s : self.set_slider_value(int(float(s))))
            
        #value = ttkb.Label(parent, textvariable=self.slider_value, font=('Helvetica', 12, 'bold'))
        label.pack(padx=10,side='left')
        self.slider.pack(padx=20,pady=20)
        #value.pack()
        self.slider_cb = cb

    def set_slider_value(self, s:int):
        self.slider_value.set(s)
        self.slider_cb(self.slider_idx)


