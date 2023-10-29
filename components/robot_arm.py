import roboticstoolbox as rtb
import numpy as np
import math
from spatialmath import SE3, SO3
import matplotlib.pyplot as plt


class RobotArm:
    def __init__(self, parent, dh_params) -> None:
        # self.robot = rtb.models.DH.Panda()
        self.parent = parent
        self.dh_params = dh_params

        self.robot = rtb.DHRobot(
            [
                rtb.RevoluteDH(d=0.07855, a=0.0, alpha=math.pi / 2),
                rtb.RevoluteDH(d=-0.0, a=0.2286, alpha=-math.pi, qlim=[-math.pi, math.pi]),
                rtb.RevoluteDH(d=0.0, a=0.0995, alpha=0, qlim=[-math.pi, math.pi]),
                rtb.RevoluteDH(d=0.0, a=0.17177, alpha=math.pi / 2, qlim=[-math.pi, math.pi])
            ]
        )
        self.robot.q = [0,math.pi/2,math.pi,-math.pi/2]

    def show_robot(self):
        self.robot.plot(self.robot.q)
