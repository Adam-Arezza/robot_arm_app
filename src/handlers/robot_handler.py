import numpy as np
from random import randint
import time
import os
import queue
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap import Frame
from src.serial_service import SerialService
from src.views.robot_view import RobotView
from src.utils import to_radians, to_degrees
from src.robot_model import RobotArm


class RobotHandler:
    def __init__(self, root, parent:Frame, serial_service:SerialService, model:RobotArm):
        self.root = root
        self.model = model
        self.serial_service = serial_service
        self.view = RobotView(root, parent)


    def show_joint_config(self, cfg:list):
        if not self.root.online_mode:
            self.set_joints(cfg)
        else:
            Messagebox.ok("Go offline to view joint configurations")
            return


    def simulate_trajectory(self, traj:list):
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
        if self.model.target and not self.model.target_reached:
            if self.check_target_reached():
                self.model.target_reached = True
                self.model.target = None
                msg = "Reached Target!"
                self.serial_service.log_msg(msg)
                if self.serial_service.command_queue.qsize() > 0:
                    self.serial_service.next_command() 
            else:
                print(f"Target: {self.model.target}")
                print(f"Current: {to_degrees(self.get_joints())}")


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
          # print(f"update joint data: {data}")
        except Exception as e:
           print("Robot Handler - Error in feedback data")
           print(e)


    def set_new_target(self, target:list):
        self.model.set_target(target)
                

    def check_target_reached(self) -> bool:
        current_joint_state = to_degrees(self.get_joints())
        #print(f"Current state: {current_joint_state}")
        #print(f"Target state: {self.model.target}")
        joints_at_position = [False for j in current_joint_state]
        for i in range(len(current_joint_state)):
            if abs(int(self.model.target[i]) - int(current_joint_state[i])) == 0:
                joints_at_position[i] = True
            else:
                joints_at_position[i] = False
        if all(joints_at_position) == True:
            return True
        else:
            return False
