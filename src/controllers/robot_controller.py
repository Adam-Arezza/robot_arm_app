from ttkbootstrap.dialogs.dialogs import Messagebox
from src.utils import to_radians, to_degrees
import numpy as np


class RobotController:
    def __init__(self):
        self.model = None
        self.view = None
        self.serial_service = None


    def add_model(self, model):
        self.model = model


    def show_joint_config(self,cfg):
        old_config = self.model.robot.q
        self.model.robot.q = to_radians(cfg)
        self.view.draw_robot(self.model.robot.q, self.model.robot)
        #self.model.robot.q = old_config


    def show_trajectory(self,traj):
        self.view.show_trajectory(traj)


    def reset(self):
        self.model.robot.q = self.model.default_state
        self.view.draw_robot(self.model.robot.q, self.model.robot)


    #given degrees, sets the radian values of the joints
    #updates the robot plot
    def set_joints(self, joints):
        if not self.model.online_mode:
            self.model.set_joint_states(to_radians(joints))
            self.update_joint_positions()
            self.update_readouts()
        else:
            separator = ':'
            serial_msg = f'<{separator.join(joints)}>'.encode()
            self.serial_service.send_serial_msg(serial_msg)

            #need to poll for feedback from potentiometers
            #update joint positions
            #update readouts


    def get_joints(self):
        return self.model.get_joints()


    def slider_callback(self):
        slider_values = []
        for slider in self.view.manual_controls.sliders:
            slider_values.append(slider.slider_value.get())
        self.set_joints(slider_values)
        #return slider_values


    def update_readouts(self):
        readouts = self.view.readouts_frame.readouts
        joint_angles = to_degrees(self.model.get_joints())
        for i in range(len(readouts)):
            readouts[i].joint_value.set(joint_angles[i])


    def toggle_auto_manual(self):
        if self.serial_service and self.serial_service.serial_connection and self.serial_service.serial_connection.is_open:
            self.model.set_mode(self.view.mode_value.get())
            if self.view.mode_value.get():
                self.view.mode_string.set('Online')
            else:
                self.view.mode_string.set('Offline')
        else:
            self.view.mode_value.set(False)
            Messagebox.ok('Must connect to serial port before going online')


#Updates the coordinates of the joints in the 3d plot
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
        self.draw_robot(joint_coordinates)


    def connect_serial_service(self, serial_service):
        self.serial_service = serial_service


    def add_view(self, view):
        self.view = view


    def draw_robot(self, joint_coords):
        self.view.draw_robot(joint_coords)


    def kill_view(self):
        self.view.close()
        self.view.destroy()
