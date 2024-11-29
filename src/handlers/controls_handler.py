from src.views.slider_controls_view import SliderControls
from ttkbootstrap.dialogs.dialogs import Messagebox
from src.utils import to_degrees
from ttkbootstrap import Frame
from src.serial_service import SerialService
from src.robot_model import RobotArm
from queue import Queue


class ControlsHandler:
    def __init__(self, root, parent:Frame, serial_service:SerialService, model:RobotArm):
        self.root = root
        self.model = model
        self.view = SliderControls(parent, slider_cb=self.slider_callback, links=self.model.links, default_state=self.model.default_state)
        self.serial_service = serial_service
        self.command_queue = Queue()

    
    def slider_callback(self, slider_idx:int):
        joint_angles = to_degrees(self.model.get_joints())
        joint_angles[slider_idx] = self.view.sliders[slider_idx].slider_value.get()
        self.model.set_joint_states(joint_angles)
        self.root.update_robot_state()
        if self.root.online_mode:
            self.serial_service.add_slider_command(joint_angles)

