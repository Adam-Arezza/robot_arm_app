import ttkbootstrap as ttkb
from src.views.components.joint_slider import JointSlider
from ttkbootstrap.constants import GROOVE

class SliderControls(ttkb.Frame):
    def __init__(self, parent, slider_cb, links):
        super().__init__(parent, borderwidth=2, relief=GROOVE)
        self.parent = parent
        self.slider_cb = slider_cb
        self.sliders = []
        for i in range(len(links)):
            slider = JointSlider(self, 
                                 f"joint_{i+1}", 
                                 self.slider_cb, 
                                 [links[i].qlim[0], links[i].qlim[1]])
            slider.pack(padx=(150,0), expand=True, fill='x')
            self.sliders.append(slider)

