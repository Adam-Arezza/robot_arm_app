import ttkbootstrap as ttk

class JointSlider(ttk.Frame):
    def __init__(self, parent, joint_name):
        super().__init__(parent)
        self.slider_value = ttk.IntVar()
        label = ttk.Label(self, text=joint_name)
        j = ttk.Scale(self, 
                          name=f'{joint_name}_slider', 
                          from_=0, 
                          to=180, 
                          value=0,
                          length=300,
                          command=lambda s : self.slider_value.set(int(float(s))))
            
        value = ttk.Label(self, textvariable=self.slider_value, font='bold')

        label.pack(side='left')
        j.pack(side='left')
        value.pack()
