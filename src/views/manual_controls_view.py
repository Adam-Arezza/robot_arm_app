import ttkbootstrap as ttkb
from src.views.components.joint_slider import JointSlider
from ttkbootstrap.constants import GROOVE

class ManualControls(ttkb.Frame):
    def __init__(self, parent, num_joints, slider_cb):
        super().__init__(parent)
        self.parent = parent
        self.slider_cb = slider_cb
        self.sliders = []
        self.num_joints = num_joints
        for i in range(self.num_joints):
            slider = JointSlider(self, f"joint_{i}", self.slider_cb)
            slider.pack()
            self.sliders.append(slider)


#    def get_slider_values(self):
#        slider_values = []
#        for slider in self.sliders:
#            slider_values.append(slider.slider_value.get())
#        return slider_values
#
    
