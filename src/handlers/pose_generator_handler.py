import numpy as np
from random import randint


class PoseGeneratorHandler:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.view.generate_btn.configure(command=self.generate)


    def generate(self):
        poses = []
        links = self.model.links
        joints = []
        num_poses = int(self.view.pose_number_input.get()) 
        save_location = self.view.save_location.get()
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
            poses.append([str(round(j[-1],3)) for j in joint_coordinates])
            joints.append([str(joint) for joint in pose_joints])
            #add euclidian distance from base to ee point
            #add roll pitch yaw of ee

        with open(f"{save_location}/pose_data.txt", "w") as data_file:
            for line in range(len(poses)):
                data = poses[line] + joints[line]
                data = str(data)              
                data_file.write(data)
                data_file.write("\n")
            data_file.close()


