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
    def __init__(self, parent, dh_params) -> None:
        # self.robot = rtb.models.DH.Panda()
        self.parent = parent
        self.dh_params = dh_params
        # print(dh_params)
        self.links = []
        for link in dh_params:
            t,a,r,d = dh_params[f'{link}']
            t = float(t)
            a = float(a)
            r = float(r)
            d = float(d)
            link = rtb.RevoluteDH(d=d, a=r, alpha=math.radians(a))
            self.links.append(link)
        self.robot = rtb.DHRobot(self.links)
        self.robot.q = [0,math.pi/2,math.pi,-math.pi/2]

    def show_robot(self):
        self.robot.plot(self.robot.q)
