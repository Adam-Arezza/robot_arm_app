from ttkbootstrap.dialogs.dialogs import Messagebox
from src.utils import to_radians, to_degrees
import numpy as np
import threading
import time


class RobotController:
    def __init__(self):
        self.model = None
        self.view = None
        self.serial_service = None
        #self.feedback_thread = threading.Thread(target=self.get_feedback, daemon=True)
        self.kill_feedback_thread = threading.Event()
        self.feedback_thread_running = False


    def show_joint_config(self,cfg):
        self.set_joints(cfg)


    def add_model(self, model):
        self.model = model


    def show_trajectory(self,traj):
        for i in traj:
            deg = to_degrees(i)
            self.set_joints(deg)
            time.sleep(0.1)


    def reset(self):
        self.model.robot.q = self.model.default_state
        self.set_joints(self.model.robot.q)


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


    def update_readouts(self, joint_angles=[]):
        joints = None
        readouts = self.view.readouts_frame.readouts
        if len(joint_angles) > 0:
            joints = joint_angles
        else:
            joints = to_degrees(self.model.get_joints())
        for i in range(len(readouts)):
            readouts[i].joint_value.set(joints[i])


    def toggle_auto_manual(self):
        if self.serial_service and self.serial_service.serial_connection and self.serial_service.serial_connection.is_open:
            self.model.set_mode(self.view.mode_value.get())
            if self.view.mode_value.get(): 
                self.feedback_thread = threading.Thread(target=self.get_feedback, daemon=True)
                self.feedback_thread_running = True
                self.feedback_thread.start()
                self.view.mode_string.set('Online')
                self.kill_feedback_thread.clear()
            else:
                self.view.mode_string.set('Offline')
                self.feedback_thread_running = False
                self.kill_feedback_thread.set()
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


    def get_feedback(self):
        while self.feedback_thread_running:
            try:
                if len(self.serial_service.message_queue) > 0:
                    data = self.serial_service.message_queue.pop(0)
                    data = data.split(":")
                    data = [int(i) for i in data]
                    data.pop()
                    self.model.set_joint_states(to_degrees(data))
                    self.update_readouts(data)
                    self.update_joint_positions()
            except Exception as e:
                print(e)
            time.sleep(0.1)
        print("stopped feedback thread")


    def kill_view(self):
        self.view.close()
        self.view.destroy()
