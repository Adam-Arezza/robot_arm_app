import ttkbootstrap as ttkb
import math
from src.views.components.joint_controller import JointController


class JointControls(ttkb.Frame):
    def __init__(self, parent, cb, links, default_state):
        super().__init__(parent)
        self.parent = parent
        self.cb = cb
        self.joints = []
        self.increment = 1

        for i in range(len(links)):
            joint_controller = JointController(self, 
                                 f"joint_{i+1}", 
                                 self.cb, 
                                 [math.degrees(links[i].qlim[0]), math.degrees(links[i].qlim[1])],
                                 default_state[i],
                                 i,
                                 self.increment)
            joint_controller.pack()          
            self.joints.append(joint_controller)

