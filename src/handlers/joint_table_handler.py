import roboticstoolbox as rtb
from src.views.components.joint_configuration_table import JointConfigurationTable
from src.utils import to_degrees, to_radians
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap.constants import *


class JointTableHandler:
    def __init__(self, root, serial_command, parent):
        self.root = root
        self.serial_connection = None
        self.serial_command = serial_command
        self.view = JointConfigurationTable(parent)
        self.view.add_to_table_btn.configure(command=self.add_configuration)
        self.view.table_btn_group.buttons["add_joint_configuration"].configure(command=self.add_joint_configuration)
        self.view.table_btn_group.buttons["show_configuration"].configure(command=self.show_configuration)
        self.view.table_btn_group.buttons["simulate_trajectory"].configure(command=self.simulate_trajectory)
        self.view.table_btn_group.buttons["send_to_robot"].configure(command=self.send_to_robot)


    def set_to_initial_state(self):
        self.root.reset_robot()


    def create_joint_entries(self,n:int):
        self.view.create_joint_entries(n)


    def add_serial_connection(self, port:str):
        self.serial_connection = port


    def remove_serial_connection(self, port:str):
        if self.serial_connection and port == '':
            self.serial_connection = None


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
            are_equal = all(i == j for i, j in zip(row.values, self.root.robot_handler.get_joints()))
            if are_equal:
                Messagebox.ok(message='The table already has this configuration')
                return 
        self.view.joint_table.insert_row(values=to_degrees(self.root.robot_handler.get_joints()))
        self.view.joint_table.load_table_data()


    def simulate_trajectory(self):
        joint_configurations = self.view.joint_table.get_rows(selected=True)
        if len(joint_configurations) != 2:
            Messagebox.ok(message='Select 2 joint configurations to compute a trajectory')
            return
        row_values = [to_radians(i.values) for i in joint_configurations]
        trajectory = rtb.jtraj(row_values[0], row_values[1], t=25)
        self.root.simulate_trajectory(trajectory.q)


    def show_configuration(self):
        config = self.view.joint_table.get_rows(selected=True)
        if len(config) > 1:
            self.view.error_msg('Select 1 joint configuration to show')
            return
        config = config[0].values
        self.root.show_configuration(config)


    def send_to_robot(self):
        if not self.root.online_mode:
            Messagebox.ok("Can't sent data to robot while offline.")
            return
        selected_row = self.view.joint_table.get_rows(selected=True)
        if len(selected_row) == 0:
            self.view.error_msg("Need to select a row to send data")
            return
        j_vals = selected_row[0].values
        j_vals = [str(i) for i in j_vals]
        separator = ':'
        serial_msg = f'<{separator.join(j_vals)}>'.encode()
        if not self.serial_connection:
            self.view.error_msg('There is no serial connection')
            return
        else:
            self.serial_command(serial_msg)

