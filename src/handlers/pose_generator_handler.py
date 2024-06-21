import numpy as np
import math
from random import randint
from src.utils import rot_mat_to_euler


class PoseGeneratorHandler:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.view.generate_btn.configure(command=self.generate)
        self.pose_data = []


    def generate(self):
        links = self.model.links
        num_poses = int(self.view.pose_number_input.get()) 
        for i in range(num_poses):
            pose_joints = []
            for j in range(len(links)):
                min_deg = links[j].qlim[0]
                max_deg = links[j].qlim[1]
                pose_joints.append(randint(min_deg,max_deg))
            self.model.set_joint_states(pose_joints)
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
            angles = rot_mat_to_euler(rot_mat).tolist()
            poses = [round(j[-1],3) for j in joint_coordinates]
            dist = [math.sqrt((poses[0]**2 + poses[1]**2 + poses[2]**2))]
            data = poses + angles + dist + pose_joints
            self.pose_data.append(data)
            self.write_pose_data()


    def write_pose_data(self):
        save_location = self.view.save_location.get()
        with open(f"{save_location}/pose_data.txt", "w") as data_file:
            for line in self.pose_data:
                data_file.write(f"{line}\n")
            data_file.close()

