import ttkbootstrap as ttkb
import math
from src.views.components.joint_slider import JointSlider


class SliderControls(ttkb.Frame):
    def __init__(self, parent, slider_cb, links, default_state):
        super().__init__(parent)
        self.parent = parent
        self.slider_cb = slider_cb
        self.sliders = []


        for i in range(len(links)):
            slider = JointSlider(self, 
                                 f"joint_{i+1}", 
                                 self.slider_cb, 
                                 [math.degrees(links[i].qlim[0]), math.degrees(links[i].qlim[1])],
                                 default_state[i],
                                 i)
            if i == 0:
                slider.pack(pady=(150,5))
            else:
                slider.pack(pady=5)
            self.sliders.append(slider)


