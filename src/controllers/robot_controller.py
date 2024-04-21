import numpy as np
import time
from ttkbootstrap.dialogs.dialogs import Messagebox
from src.views.robot_view import RobotView
from src.utils import to_radians, to_degrees
from src.models.robot_model import RobotArm
from src.serial_service import SerialService


class RobotController:
    def __init__(self, root, parent, serial_command):
        self.root = root
        self.model = None
        self.serial_command = serial_command
        self.view = RobotView(root, parent)
        self.view.toggle_mode_switch.configure(command=self.toggle_online_offline)
        self.view.reset_btn.configure(command=self.reset)
        self.serial_connected = None


    def show_joint_config(self,cfg:list):
        if not self.model.online_mode:
            self.set_joints(cfg)
        else:
            Messagebox.ok("Go offline to view joint configurations")
            return

    def add_model(self, model:RobotArm):
        self.model = model
        self.view.add_controls(self.slider_callback, self.model.robot.links)


    def simulate_trajectory(self,traj:list):
        if self.model.online_mode:
            Messagebox.ok("Must be in offline mode")
            return
        for i in traj:
            deg = to_degrees(i)
            self.set_joints(deg)
            time.sleep(0.025)


    def reset(self):
        self.model.robot.q = self.model.default_state
        self.set_joints(self.model.robot.q)
        sliders = self.view.slider_controls.sliders
        for i in range(len(sliders)):
            sliders[i].slider_value.set(self.model.default_state[i])
            sliders[i].slider.set(self.model.default_state[i])


    def set_joints(self, joints:list):
        self.model.set_joint_states(joints)
        self.update_joint_positions()
        self.update_readouts()
            #joints = [str(i) for i in joints]
            #separator = ':'
            #serial_msg = f'<{separator.join(joints)}>'.encode()
            #self.serial_command(serial_msg)


    def get_joints(self) -> list:
        return self.model.get_joints()


    def slider_callback(self):
        slider_values = []
        for slider in self.view.slider_controls.sliders:
            slider_values.append(slider.slider_value.get())
        self.set_joints(slider_values)


    def update_readouts(self):
        joints = self.model.get_joints()
        readouts = self.view.readouts_frame.readouts
        joints = to_degrees(self.model.get_joints())
        for i in range(len(readouts)):
            readouts[i].joint_value.set(joints[i])


    def toggle_online_offline(self):
        if self.serial_connected:
            self.model.set_mode(self.view.mode_value.get())
            self.root.set_online_mode(self.view.mode_value.get())
            self.send_connected_msg()
            self.reset()
        else:
            self.view.mode_value.set(False)
            Messagebox.ok('Must connect to serial port before going online')


    def add_serial_connection(self, port:str):
        self.serial_connected = port


    def remove_serial_connection(self, port:str):
        self.serial_connected = port
        self.view.mode_value.set(False)
        self.model.set_mode(False)


    def send_connected_msg(self):
        if self.view.mode_value.get(): 
            self.view.mode_string.set('Online')
            go_online_msg = f'<online>'.encode()
            self.serial_command(go_online_msg)
        else:
            self.view.mode_string.set('Offline')


    def update_joint_positions(self):
        joint_angles = self.model.get_joints()
        prev_transform = None
        joint_coordinates = [[0],[0],[0]]
        for i in range(len(joint_angles)):
            t_matrix = self.model.robot.links[i].A(self.model.robot.q[i])  
            t_matrix = np.array(t_matrix)
            new_transform = t_matrix
            if i > 0:
                new_transform = np.dot(prev_transform, t_matrix)

            prev_transform = new_transform
            j_coords = new_transform[:3,3]
            joint_coordinates[0].append(j_coords[0])
            joint_coordinates[1].append(j_coords[1])
            joint_coordinates[2].append(j_coords[2])
        self.view.draw_robot(joint_coordinates)


    def update_joint_data(self, new_data:str):
        try:
            data = new_data.strip()
            data = data.split(":")
            data = [int(i) for i in data]
            data.pop()
            self.set_joints(data)
        except Exception as e:
            print("Robot Controller - Error in feedback data")
            print(e)


