import roboticstoolbox as rtb
import numpy as np
import math
from spatialmath import SE3, SO3
import matplotlib.pyplot as plt


# DH parameters of robot arm
# Joint	θ	α	r	d
#   1	θ1	90	0.0	0.07855
#   2	θ2 -180 0.2286	0.0
#   3	θ3	0	0.0995	0.0
#   4	θ4	90	0.17177	0.0

class RobotArm:
    def __init__(self, dh_params, mode, initial_joint_states = []) -> None:
        self.links = []
        self.dh_params = dh_params
        self.target = None 
        self.default_state = [0,0,0,0]
        self.online_mode = mode
        if len(dh_params) > 0:
           self.create_robot_from_dh(dh_params, initial_joint_states)


    def set_joint_states(self,joint_states):
        self.robot.q = joint_states


    def set_mode(self, mode):
        self.online_mode = mode


    def get_joints(self):
        return self.robot.q


    def create_robot_from_dh(self, dh_params, initial_joint_states):
        for i,link in enumerate(dh_params):
            # add the joint limits to the link
            t,a,r,d = dh_params[f'{link}']
            t = float(t)
            a = float(a)
            r = float(r)
            d = float(d)
            link = rtb.RevoluteDH(d=d, a=r, alpha=math.radians(a))
            self.links.append(link)
        self.robot = rtb.DHRobot(self.links) 
        if len(initial_joint_states) != len(self.links):
            self.robot.q = [0 for i in self.links]
        else:
            self.robot.q = initial_joint_states
            self.default_state = initial_joint_states
