from src.utils import to_radians
import numpy as np


class RobotController:
    def __init__(self):
        self.model = None
        self.view = None


    def add_model(self, model):
        self.model = model


    def teach_pendant(self):
        self.model.robot.teach(self.model.robot.q)


    def show_joint_config(self,cfg):
        old_config = self.model.robot.q
        self.model.robot.q = to_radians(cfg)
        self.view.draw_robot(self.model.robot.q, self.model.robot)
        #self.model.robot.q = old_config


    def show_trajectory(self,traj):
        self.view.show_trajectory(traj)


    def reset(self):
        self.model.robot.q = self.model.default_state
        self.view.draw_robot(self.model.robot.q, self.model.robot)


    def set_joints(self, joints):
        self.model.robot.q = joints


    def get_joints(self):
        return self.model.robot.q


    def add_view(self, view):
        self.view = view


    def draw_robot(self):
        self.view.draw_robot(self.model.robot.q, self.model.robot)


    def kill_view(self):
        self.view.close()
        self.view.destroy()
