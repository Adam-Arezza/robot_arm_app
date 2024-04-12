import ttkbootstrap as ttkb
from src.views.components.joint_slider import JointSlider
from ttkbootstrap.constants import GROOVE

class ManualControls(ttkb.Frame):
    def __init__(self, parent, slider_cb, links):
        super().__init__(parent)
        self.parent = parent
        self.slider_cb = slider_cb
        self.sliders = []
        for i in range(len(links)):
            slider = JointSlider(self, 
                                 f"joint_{i+1}", 
                                 self.slider_cb, 
                                 [links[i].qlim[0], links[i].qlim[1]])
            slider.pack()
            self.sliders.append(slider)

