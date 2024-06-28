import roboticstoolbox as rtb
import numpy as np
import time
from src.views.components.joint_configuration_table import JointConfigurationTable
from src.utils import to_degrees, to_radians
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap.constants import *


class JointTableHandler:
    def __init__(self, root, serial_service, parent):
        self.root = root
        self.serial_service = serial_service
        self.view = JointConfigurationTable(parent)
        self.view.add_to_table_btn.configure(command=self.add_configuration)
        self.view.table_btn_group.buttons["add_joint_configuration"].configure(command=self.add_joint_configuration)
        self.view.table_btn_group.buttons["show_configuration"].configure(command=self.show_configuration)
        self.view.table_btn_group.buttons["simulate_trajectory"].configure(command=self.simulate_trajectory)
        self.view.table_btn_group.buttons["send_to_robot"].configure(command=self.send_to_robot)
        self.view.table_btn_group.buttons["save_trajectory_data"].configure(command=self.save_trajectory_data)
        self.view.table_btn_group.buttons["clear_table"].configure(command=self.clear_table)


    def set_to_initial_state(self):
        self.root.reset_robot()


    def create_joint_entries(self,n:int):
        self.view.create_joint_entries(n)


    def add_configuration(self): 
        joint_values = []
        for p in self.view.joint_config_entry.params:
            val = p.get()
            val = int(float(val))
            joint_values.append(val)
            p.set(str(0))
        self.view.joint_table.insert_row(values=joint_values) 
        self.view.joint_table.load_table_data()
        

    def add_joint_configuration(self):
        rows = self.view.joint_table.get_rows(visible=True)
        for row in rows:
            are_equal = all(i == j for i, j in zip(row.values, self.root.robot_model.get_joints()))
            if are_equal:
                Messagebox.ok(message='The table already has this configuration')
                return 
        self.view.joint_table.insert_row(values=to_degrees(self.root.robot_model.get_joints()))
        self.view.joint_table.load_table_data()


    def simulate_trajectory(self):
        trajectory = self.generate_trajectory()
        self.root.simulate_trajectory(trajectory)


    def generate_trajectory(self):
        final_trajectory = None
        joint_configurations = self.view.joint_table.get_rows(selected=True)
        if len(joint_configurations) < 2:
            Messagebox.ok(message='Select at least 2 joint configurations to compute a trajectory')
            return
        row_values = [to_radians(i.values) for i in joint_configurations]
        for i in range(len(row_values)):
            if i == 0:
                continue
            partial_trajectory = rtb.jtraj(row_values[i-1],row_values[i], t=25)
            #print(partial_trajectory.q)
            if i == 1:
                final_trajectory = partial_trajectory.q
            else:
                final_trajectory = np.concatenate((final_trajectory,partial_trajectory.q), axis=0)
        return final_trajectory


    def show_configuration(self):
        config = self.view.joint_table.get_rows(selected=True)
        if len(config) > 1:
            self.view.error_msg('Select 1 joint configuration to show')
            return
        config = config[0].values
        self.root.show_configuration(config)


    def send_to_robot(self):
        selected_rows = self.view.joint_table.get_rows(selected=True)
        new_trajectory = [i.values for i in selected_rows]
        for trajectory in new_trajectory:
            print(trajectory)

        if not self.serial_service.serial_connection:
            self.view.error_msg('There is no serial connection')
            return

        if not self.root.online_mode:
            Messagebox.ok("Can't sent data to robot while offline.")
            return

        if len(selected_rows) == 0:
            self.view.error_msg("Need to select one or more rows to send data")
            return

        self.serial_service.start_command_queue(new_trajectory)
                

    def clear_table(self):
        self.view.joint_table.delete_rows()


    def save_trajectory_data(self):
        self.view.joint_table.export_all_records()

