from src.views.controls_view import ControlsView
from ttkbootstrap.dialogs.dialogs import Messagebox


class ControlsController:
    def __init__(self, root, parent, serial_command, model):
        self.root = root
        self.model = model
        self.view = ControlsView(parent, self.slider_callback, self.model.robot.links)
        self.serial_connected = None
        self.serial_command = serial_command
        self.view.toggle_mode_switch.configure(command=self.toggle_online_offline)
        self.view.reset_btn.configure(command=self.reset)


    def add_serial_connection(self, port:str):
        self.serial_connected = port


    def slider_callback(self):
        slider_values = []
        for slider in self.view.slider_controls.sliders:
            slider_values.append(slider.slider_value.get())
        self.model.set_joint_states(slider_values)
        if not self.root.online_mode:
            self.root.update_robot_state()


    def toggle_online_offline(self):
        if self.serial_connected:
            self.root.set_online_mode(self.view.mode_value.get())
            self.send_connected_msg()
            self.reset()
        else:
            self.view.mode_value.set(False)
            Messagebox.ok('Must connect to serial port before going online')


    def reset(self):
        self.model.set_joint_states(self.model.default_state)
        sliders = self.view.slider_controls.sliders
        for i in range(len(sliders)):
            sliders[i].slider_value.set(self.model.default_state[i])
            sliders[i].slider.set(self.model.default_state[i])
        self.root.update_robot_state()


    def send_connected_msg(self):
        if self.view.mode_value.get(): 
            self.view.mode_string.set('Online')
            go_online_msg = f'<online>'.encode()
            self.serial_command(go_online_msg)
        else:
            self.view.mode_string.set('Offline')

