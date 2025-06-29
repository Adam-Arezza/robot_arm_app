from src.views.joint_controls_view import JointControls
from ttkbootstrap.dialogs.dialogs import Messagebox
from src.utils import to_degrees
from ttkbootstrap import Frame
from src.robot_model import RobotArm
from queue import Queue

#TODO
#add end effector controls (move in x y z directions)

class ControlsHandler:
    def __init__(self, root, parent:Frame, model:RobotArm):
        self.root = root
        self.model = model
        self.view = JointControls(parent, cb=self.slider_callback, links=self.model.links, default_state=self.model.default_state)

    
    def slider_callback(self, slider_idx:int):
        joint_angles = to_degrees(self.model.get_joints())
        joint_angles[slider_idx] = self.view.sliders[slider_idx].slider_value.get()
        self.model.set_joint_states(joint_angles)
        self.root.update_robot_state()

