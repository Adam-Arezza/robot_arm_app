import numpy as np
from random import randint
import time
import os
from ttkbootstrap.dialogs.dialogs import Messagebox
from src.views.robot_view import RobotView
from src.utils import to_radians, to_degrees
from src.robot_model import RobotArm
from src.serial_service import SerialService


class RobotHandler:
    def __init__(self, root, parent, serial_command, model):
        self.root = root
        self.model = model
        self.serial_command = serial_command
        self.view = RobotView(root, parent)
        self.serial_connected = None


    def show_joint_config(self,cfg:list):
        if not self.root.online_mode:
            self.set_joints(cfg)
        else:
            Messagebox.ok("Go offline to view joint configurations")
            return


    def simulate_trajectory(self,traj:list):
        if self.root.online_mode:
            Messagebox.ok("Must be in offline mode")
            return
        for i in traj:
            deg = to_degrees(i)
            self.set_joints(deg)
            time.sleep(0.025)


    def set_joints(self, joints:list):
        self.model.set_joint_states(joints)
        self.update_joint_positions()


    def get_joints(self) -> list:
        return self.model.get_joints()


    def update_joint_positions(self):
        joint_angles = self.model.get_joints()
        prev_transform = None
        joint_coordinates = [[0],[0],[0]]
        rot_mat = None
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
            if i == len(joint_angles)-1:
                rot_mat = new_transform[:3,:3]
        self.view.draw_robot(self.model.robot.q, joint_coordinates, rot_mat)


    def update_joint_data(self, new_data:str):
        try:
            data = new_data.strip()
            data = data.split(":")
            data = [int(i) for i in data]
            data.pop()
            self.set_joints(data)
        except Exception as e:
            print("Robot Handler - Error in feedback data")
            print(e)

