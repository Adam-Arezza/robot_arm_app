import numpy as np
from random import randint
import time
import os
from src.utils import rot_mat_to_euler
import math
from ttkbootstrap.dialogs.dialogs import Messagebox
from src.views.robot_view import RobotView
from src.utils import to_radians, to_degrees
from src.models.robot_model import RobotArm
from src.serial_service import SerialService


class RobotController:
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
        joint_coordinates, rot_mat = self.model.get_ee_pose()
        if data_gen:
            self.euler_angles = rot_mat_to_euler(rot_mat)
            self.joint_coordinates = joint_coordinates
        else:
            self.view.draw_robot(joint_coordinates, rot_mat)


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


    def generate_pose_data(self):
        poses = []
        links = self.model.links
        joints = []
        angles = []
        dist_to_base = []
        for i in range(80000):
            pose_joints = []
            for j in range(len(links)):
                min_deg = links[j].qlim[0]
                max_deg = links[j].qlim[1]
                pose_joints.append(randint(min_deg,max_deg))
            self.set_joints(pose_joints, data_gen=True)
            poses.append([str(round(j[-1],3)) for j in self.joint_coordinates])
            joints.append([str(joint) for joint in pose_joints])
            angles.append([str(angle) for angle in self.euler_angles])
            d_to_b = math.sqrt(float(poses[i][0])**2 + float(poses[i][1])**2 + float(poses[i][2])**2)
            dist_to_base.append([str(d_to_b)])
            print(f"finished {i}")
        if "pose_data.txt" in os.listdir("test\\"):
            os.remove("test\\pose_data.txt")
        with open("test/pose_data.txt", "a") as data_file:
            for line in range(len(poses)):
                data = poses[line] + angles[line] + dist_to_base[line] + joints[line]
                data = str(data)              
                data_file.write(data)
                data_file.write("\n")
            data_file.close()


    def generate_square(self, square_dims:tuple, solver):
        #define the corners of the square
        #use rtb IK to generate the joint angles for the corners
        #use rtb traj to generate the points between the corners
        #store all points starting from one corner and ending at the same corner
        #simulate the trajectory of the robot
        #include the points in the simulation for visualizing the path
        pass

    def generate_circle(self):

        pass
