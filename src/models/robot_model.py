import roboticstoolbox as rtb
import numpy as np
import math
import matplotlib.pyplot as plt
from src.utils import to_radians
from spatialmath import SE3, SO3


class RobotArm:
    def __init__(self, dh_params, mode, initial_joint_states = []) -> None:
        self.links = []
        self.dh_params = dh_params
        self.target = None 
        self.default_state = []
        self.online_mode = mode
        if len(dh_params) > 0:
           self.create_robot_from_dh(dh_params, initial_joint_states)


    def set_joint_states(self, joint_states:list):
        rads = to_radians(joint_states)
        self.robot.q = rads


    def set_mode(self, mode:bool):
        self.online_mode = mode


    def get_joints(self) -> list:
        return self.robot.q


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
