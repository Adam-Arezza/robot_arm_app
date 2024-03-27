import ttkbootstrap as ttkb

class JointSlider(ttkb.Frame):
    def __init__(self, parent, joint_name):
        super().__init__(parent)
        self.slider_value = ttkb.IntVar()
        label = ttkb.Label(self, text=joint_name.replace("_", " ").capitalize())
        j = ttkb.Scale(self, 
                          name=f'{joint_name}_slider', 
                          from_=0, 
                          to=180, 
                          value=0,
                          command=lambda s : self.slider_value.set(int(float(s))))
            
        value = ttkb.Label(self, textvariable=self.slider_value, font='bold')

        label.pack(side='left')
        j.pack(side='left')
        value.pack()
