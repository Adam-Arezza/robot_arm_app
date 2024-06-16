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
        self.view.gen_data_btn.configure(command=self.generate_pose_data)
        self.serial_connected = None
        self.joint_coordinates = []


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


    def set_joints(self, joints:list, data_gen:bool = False):
        self.model.set_joint_states(joints)
        self.update_joint_positions(data_gen = data_gen)


    def get_joints(self) -> list:
        return self.model.get_joints()


    def update_joint_positions(self, data_gen:bool = False):
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
        if data_gen:
            self.joint_coordinates = joint_coordinates
        else:
            #print(f"final transformation matrix: {rot_mat}")
            self.view.draw_robot(joint_coordinates, rot_mat)


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


    def generate_pose_data(self):
        poses = []
        links = self.model.links
        joints = []
        for i in range(20000):
            pose_joints = []
            for j in range(len(links)):
                min_deg = links[j].qlim[0]
                max_deg = links[j].qlim[1]
                pose_joints.append(randint(min_deg,max_deg))
            self.set_joints(pose_joints, data_gen=True)
            poses.append([str(round(j[-1],3)) for j in self.joint_coordinates])
            joints.append([str(joint) for joint in pose_joints])
        if "pose_data.txt" in os.listdir("test\\"):
            os.remove("test\\pose_data.txt")
        with open("test/pose_data.txt", "a") as data_file:
            for line in range(len(poses)):
                data = poses[line] + joints[line]
                data = str(data)              
                data_file.write(data)
                data_file.write("\n")
            data_file.close()

