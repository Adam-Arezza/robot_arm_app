import numpy as np
import time
import spatialmath as sm
import roboticstoolbox as rtb
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap import Frame
from src.serial_service import SerialService
from src.views.robot_view import RobotView
from src.utils import to_degrees
from src.robot_model import RobotArm


class RobotHandler:
    def __init__(self, root, parent:Frame, serial_service:SerialService, model:RobotArm):
        self.root = root
        self.model = model
        self.serial_service = serial_service
        self.view = RobotView(parent)


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
            #print(i)
            deg = to_degrees(i)
            #print(deg)
            self.set_joints(deg)
            self.serial_service.log_msg(f"Moving to: {i}", "INFO")
            time.sleep(0.025)


    def set_joints(self, joints:list):
        self.model.set_joint_states(joints)
        if not self.root.online_mode:
            self.update_joint_positions()
        if self.model.target and not self.model.target_reached:
            if self.check_target_reached():
                self.model.target_reached = True
                self.model.target = None
                msg = "Reached Target!"
                self.serial_service.log_msg(msg, "INFO")
                if self.serial_service.command_queue.qsize() > 0:
                    self.serial_service.next_command() 


    def get_joints(self) -> list:
        return self.model.get_joints()


    def update_joint_positions(self):
        rot_mat = None
        prev_transform = None
        joint_coordinates = [[0],[0],[0]]
        for i in range(len(self.model.links)):
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
        rot_mat = new_transform[:3,:3]
        self.view.draw_robot(self.model.robot.q, joint_coordinates, rot_mat)


    def update_joint_data(self, new_data:str):
        try:
            data = new_data.strip()
            data = data.split(":")
            data = [int(i) for i in data]
            data.pop()
            self.set_joints(data)
        except Exception as e:
            self.serial_service.log_msg(f"There was an error updating joint data -> {e}", "ERROR")
            print("Robot Handler - Error in feedback data")
            print(e)


    def set_new_target(self, target:list):
        self.model.set_target(target)


    def check_target_reached(self) -> bool:
        current_joint_state = to_degrees(self.get_joints())
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


    def add_goal_point(self, point):
        point = [float(point[i]) for i in range(len(point))]
        #self.model.add_goal_point(point)
        self.view.draw_point(point, False)


    def go_to_goal(self, goal:list):
        robot = self.model.robot
        #TODO
        #get points from goal
        #create a trajectory from point to point
        #simulate trajectory
        #if online, send to robot
        #point = self.model.goal_point
        previous_point = self.model.robot.q
        for point in goal:
            T_trans = sm.SE3(point[0], point[1], point[2])
            solution = robot.ikine_LM(Tep=T_trans, q0=previous_point, mask=[1,1,1,0,0,0], joint_limits=True) 
            trajectory = self.generate_trajectory(robot, solution)
            self.simulate_trajectory(trajectory)


    def generate_trajectory(self, robot, goal_pose) -> np.ndarray:
        #print(f"Current position: {robot.q}")
        #print(f"Goal position: {goal_pose.q}")
        trajectory = rtb.jtraj(robot.q, goal_pose.q, t=25)
        return trajectory.q


    def preview_point(self, point):
        point = [round(float(point[i]), 3) for i in range(len(point))]
        self.view.draw_point(point, True)


    def clear_point_preview(self):
        self.view.clear_point_preview()

    
    def check_valid_point(self, point) -> bool:
        robot = self.model.robot
        point = [float(point[i]) for i in range(len(point))]
        T_trans = sm.SE3(point[0], point[1], point[2])
        T_rot = sm.SO3.RPY(0,0,0, unit='rad') 
        T = T_trans * sm.SE3(T_rot)
        solution = robot.ikine_LM(Tep=T_trans, q0=self.model.robot.q, mask=[1,1,1,0,0,0], joint_limits=True) 
        if solution.success:
            return True
        else:
            return False


    def ccd_ik(self, target):
        pass

    
    def fabrik_ik(self, target):
        rot_mat = None
        prev_transform = None
        joint_coordinates = [np.array([0,0,0])]
        link_lengths = []
        for i in range(len(self.model.links)):
            t_matrix = self.model.robot.links[i].A(self.model.robot.q[i])  
            t_matrix = np.array(t_matrix)
            new_transform = t_matrix
            if i > 0:
                new_transform = np.dot(prev_transform, t_matrix)
            prev_transform = new_transform
            j_coords = new_transform[:3,3]
            joint_coordinates.append(j_coords)
            rot_mat = new_transform[:3,:3]
            link_lengths.append(round(np.linalg.norm(j_coords - joint_coordinates[i]),3))

        #determine if the target point is reachable (at least doesn't extend further than the full extent of links)
        target_distance = np.linalg.norm(target - joint_coordinates[0])
        total_reach = np.sum(link_lengths)
        if target_distance > total_reach:
            self.serial_service.log_msg("target is not reachable", "INFO")
            return
        else:
            root = joint_coordinates[0]
            dist_to_target = np.linalg.norm(joint_coordinates[-1] - target)
            tolerance = 0.1
            while dist_to_target > tolerance:

                #backwards pass
                joint_coordinates[-1] = target
                for i in reversed(range(len(link_length))):
                    #new vector from the target to the next joint
                    #the joint will be placed on this new vector link length distance from target
                    new_vec = np.linalg.norm(joint_coordinates[i] - joint_coordinates[i-1])
                    joint_coordinates[i - 1] = joint_coordinates[i] + link_lengths[i] * (joint_coordinates[i] / new_vec)

                #forwards pass
                for j in range(len(link_lengths)):
                    joint_coordinates[j] = root
                    new_vec = np.linalg.norm(joint_coordinates[i] - joint_coordinates[i+1])
                    joint_coordinates[i + 1] = joint_coordinates[i] + link_lengths[i] * (joint_coordinates[i] / new_vec) 
                dist_to_target = np.linalg.norm(joint_coordinates[-1] - target)
                
