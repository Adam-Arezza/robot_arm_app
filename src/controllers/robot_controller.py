from src.utils import to_radians
import numpy as np


class RobotController:
    def __init__(self, view, model):
        self.view = view
        self.model = model

    def show_robot(self):
        self.model.robot.plot(self.model.robot.q)

    def teach_pendant(self):
        self.model.robot.teach(self.model.robot.q)

    def show_joint_config(self,cfg):
        old_config = self.model.robot.q
        self.model.robot.q = to_radians(cfg)
        self.model.robot.plot(self.model.robot.q)
        self.model.robot.q = old_config

    def show_trajectory(self,traj):
        self.model.robot.plot(traj)


    def reset(self):
        self.model.robot.q = self.model.default_state


    def set_joints(self, joints):
        self.model.robot.q = joints
        print(self.model.robot.q)


    def get_joints(self):
        print(self.model.robot.q)
        return self.model.robot.q

    def show_view(self):
        self.view.pack(anchor='ne', side='right', fill='x', padx=0, pady=0)
        print(self.model.robot)
        print(f"Link Lengths: {self.model.robot.a}")
        print(f"Robot Reach: {self.model.robot.reach}")
        print(self.model.robot.alpha)
        #print(self.model.robot.fkine(self.model.robot.q))
        #print(self.model.robot.A([0,1],self.model.robot.q))
        #print(self.model.robot.A([1,2],self.model.robot.q))
        #print(self.model.robot.A([2,3],self.model.robot.q))
        self.view.draw_robot(self.model.robot.q, self.model.robot)


    def kill_view(self):
        self.view.close()
        self.view.destroy()
