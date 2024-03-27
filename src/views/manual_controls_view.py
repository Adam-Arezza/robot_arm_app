import ttkbootstrap as ttkb
from src.views.components.joint_slider import JointSlider
from ttkbootstrap.constants import GROOVE

class ManualControls(ttkb.Frame):
    def __init__(self, parent, num_joints):
        super().__init__(parent, borderwidth=2, relief=GROOVE)
        self.sliders = []
        self.num_joints = num_joints
        for i in range(self.num_joints):
            slider = JointSlider(self, f"joint_{i}")
            slider.pack()
            self.sliders.append(slider)




