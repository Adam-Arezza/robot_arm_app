import roboticstoolbox as rtb
from src.views.components.joint_configuration_table import JointConfigurationTable
from src.utils import to_degrees, to_radians
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap.constants import *


class JointTableController:
    def __init__(self, root, parent, num_joints):
        self.view = JointConfigurationTable(parent, self, num_joints)
        self.root = root


    def show_view(self):
        self.view.pack_propagate(0)
        self.view.pack(expand=True, padx=0, pady=0, fill='both')


    def kill_view(self):
        self.view.destroy()


    def set_to_initial_state(self):
        self.root.reset_robot()


    def add_configuration(self): 
        joint_values = []
        for p in self.view.joint_config_entry.params:
            val = p.get()
            val = int(float(val))
            joint_values.append(val)
        self.view.joint_table.insert_row(values=joint_values) 
        self.view.joint_table.load_table_data()
        self.root.robot_controller.set_joints(to_radians(joint_values))
        for p in self.view.joint_config_entry.params:
            p.set(str(0)) 

    def add_joint_configuration(self):
        rows = self.view.joint_table.get_rows(visible=True)
        for row in rows:
            are_equal = all(i == j for i, j in zip(row.values, self.root.robot_controller.get_joints()))
            if are_equal:
                Messagebox.ok(message='The table already has this configuration')
                return 
        self.view.joint_table.insert_row(values=to_degrees(self.root.robot_controller.get_joints()))
        self.view.joint_table.load_table_data()

    def show_trajectory(self):
        joint_configurations = self.view.joint_table.get_rows(selected=True)
        if len(joint_configurations) != 2:
            Messagebox.ok(message='Select 2 joint configurations to compute a trajectory')
            return
        row_values = [to_radians(i.values) for i in joint_configurations]
        trajectory = rtb.jtraj(row_values[0], row_values[1], t=25)
        self.root.show_trajectory(trajectory.q)


    def show_configuration(self):
        config = self.view.joint_table.get_rows(selected=True)
        if len(config) > 1:
            Messagebox.ok(message='Select 1 joint configuration to show')
            return
        config = config[0].values
        self.root.show_configuration(config)
