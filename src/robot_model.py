import roboticstoolbox as rtb
import numpy as np
import math
import matplotlib.pyplot as plt
from src.utils import to_radians, rot_mat_to_euler


class RobotArm:
    def __init__(self, dh_params, mode, initial_joint_states = []) -> None:
        self.links = []
        self.dh_params = dh_params
        self.target = None 
        self.default_state = []
        self.joint_coordinates = []

        if len(dh_params) > 0:
           self.create_robot_from_dh(dh_params, initial_joint_states)


    def set_joint_states(self, joint_states:list):
        rads = to_radians(joint_states)
        self.robot.q = rads


    def get_joints(self) -> list:
        return self.robot.q
   

    def get_ee_pose(self) -> list:
        joint_angles = self.get_joints()
        joint_coordinates = [[0],[0],[0]]
        rot_mat = None
        for i in range(len(joint_angles)):
            t_matrix = self.links[i].A(self.robot.q[i])  
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

        return joint_coordinates, rot_mat


    def create_robot_from_dh(self, dh_params:dict, initial_joint_states:list):
        for i,link in enumerate(dh_params):
            t,a,r,d,ql,qu = dh_params[f'{link}']
            t = float(t)
            a = float(a)
            r = float(r)
            d = float(d)
            ql = float(ql)
            qu = float(qu)
            link = rtb.RevoluteDH(d=d, a=r, alpha=math.radians(a), qlim=[ql,qu])
            self.links.append(link)

        self.robot = rtb.DHRobot(self.links) 
        if len(initial_joint_states) != len(self.links):
            self.robot.q = [0 for i in self.links]
            self.default_state = [0 for i in self.links]
        else:
            self.robot.q = initial_joint_states
            self.default_state = initial_joint_states
