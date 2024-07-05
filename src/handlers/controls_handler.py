from src.views.controls_view import ControlsView
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
        self.view = ControlsView(parent, self.slider_callback, self.model.robot.links, self.model.default_state)
        self.serial_service = serial_service
        self.view.toggle_mode_switch.configure(command=self.toggle_online_offline)
        self.view.reset_btn.configure(command=self.reset)
        self.command_queue = Queue()

    
    def slider_callback(self, slider_idx:int):
        joint_angles = to_degrees(self.model.get_joints())
        joint_angles[slider_idx] = self.view.slider_controls.sliders[slider_idx].slider_value.get()
        self.model.set_joint_states(joint_angles)
        self.root.update_robot_state()
        if self.root.online_mode:
            self.serial_service.add_slider_command(joint_angles)


    def toggle_online_offline(self):
        if self.serial_service.serial_connection:
            self.root.set_online_mode(self.view.mode_value.get())
            self.send_connected_msg()
            self.reset()
        else:
            self.view.mode_value.set(False)
            Messagebox.ok('Must connect to serial port before going online')


    def reset(self):
        print("resetting")
        self.model.set_joint_states(self.model.default_state)
        sliders = self.view.slider_controls.sliders
        for i in range(len(sliders)):
            sliders[i].slider_value.set(self.model.default_state[i])
            sliders[i].slider.set(self.model.default_state[i])
        if not self.root.online_mode:
            self.root.update_robot_state()
        else:
            command = self.serial_service.format_msg(self.model.default_state)
            self.serial_service.send_serial_msg(command)


    def send_connected_msg(self):
        if self.view.mode_value.get(): 
            self.view.mode_string.set('Online')
            go_online_msg = f'<online>'.encode()
            self.serial_service.send_serial_msg(go_online_msg)
        else:
            self.view.mode_string.set('Offline')

