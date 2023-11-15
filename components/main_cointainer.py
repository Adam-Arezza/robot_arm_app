import ttkbootstrap as ttk
import roboticstoolbox as rtb
from ttkbootstrap.dialogs.dialogs import Messagebox
from components.robot_config import RobotConfig
from components.table_row import TableRow
from components.joint_config import JointConfig
from components.button_group import ButtonGroup
import math
from components.joint_configuration_table import JointConfigurationTable
from PIL import Image
Image.CUBIC = Image.BICUBIC

class MainContainer(ttk.Frame):
    def __init__(self, parent, name, robot_arm):
        super().__init__(parent, name=name, width=700)
        self.robot_arm = robot_arm
        self.joint_config_list = []
        self.selected_joint_configurations = []
        self.default_joint_state = self.robot_arm.robot.q
       
        self.top_frame = ttk.Frame(self)
        self.headers = ['Theta (deg)', 'Alpha (deg)', 'r (m)', 'd (m)']    
        self.robot_config = RobotConfig(self.top_frame, robot_arm.dh_params, self.headers)
        self.robot_config.pack(side='left') 

        self.initial_joint_state = ttk.StringVar()
        self.previous_joint_state = ttk.StringVar()
        self.current_joint_state = ttk.StringVar()

        self.initial_joint_state.set(str(self.to_degrees(robot_arm.robot.q)))

        self.initial_joints = JointConfig(self.top_frame, 'Initial Joint State',
                                          self.initial_joint_state)
        self.previous_joints = JointConfig(self.top_frame, 'Previous Joint State',
                                           self.previous_joint_state)
        self.current_joints = JointConfig(self.top_frame, 'Current Joint State',
                                           self.current_joint_state)
        
        self.initial_joints.pack()
        self.previous_joints.pack()
        self.current_joints.pack()

        self.top_frame.pack(fill='x')

        self.table_btn_group = ButtonGroup(self, [('Update Joints', self.update_joint_configs),
                                                  ('Add Joint Configuration', self.add_joint_configuration),
                                                  ('Show Configuration', self.show_configuration),
                                                  ('Show Trajectory', self.show_trajectory),
                                                  ('Re-initialize', self.set_to_initial_state)],
                                                  style='info')

        self.table_btn_group.pack(anchor='nw', pady=(40,5), padx=5)

# Joint entry
        self.joint_entry_frame = ttk.Frame(self)
        self.joint_config_entry = TableRow(self.joint_entry_frame, 'Configure Joints')
        self.joint_config_entry.pack(side='left', pady=15)

        self.add_to_table_btn = ttk.Button(self.joint_entry_frame, text='Add to table', command=self.add_configuration, bootstyle='success')
        self.add_to_table_btn.pack(pady=15)

        self.joint_entry_frame.pack()

#Joint configuration table
        self.joint_config_table = JointConfigurationTable(self, self.to_degrees(self.robot_arm.robot.q))
        self.joint_config_table.pack() 
 
    def to_degrees(self, radians:list):
        result = []
        for i in radians:
            result.append(round(math.degrees(i)))
        return result

    def to_radians(self, degrees:list):
        result = []
        for i in degrees:
            result.append(math.radians(i))
        return result

    def set_to_initial_state(self):
        self.robot_arm.robot.q = self.default_joint_state

    def update_joint_configs(self):
        self.previous_joint_state.set(self.current_joint_state.get())
        self.current_joint_state.set(str(self.to_degrees(self.robot_arm.robot.q))) 

    def add_joint_configuration(self):
        rows = self.joint_config_table.joint_table.get_rows(visible=True)
        for row in rows:
            are_equal = all(i == j for i, j in zip(row.values, self.robot_arm.robot.q))
            if are_equal:
                Messagebox.ok(message='The table already has this configuration')
                return 
        self.joint_config_table.joint_table.insert_row(values=self.to_degrees(self.robot_arm.robot.q))
        self.joint_config_table.joint_table.load_table_data()
        self.update_joint_configs()
    
    def show_trajectory(self):
        joint_configurations = self.joint_config_table.joint_table.get_rows(selected=True)
        if len(joint_configurations) != 2:
            Messagebox.ok(message='Select 2 joint configurations to compute a trajectory')
            return
        row_values = [self.to_radians(i.values) for i in joint_configurations]
        trajectory = rtb.jtraj(row_values[0], row_values[1], t=25)
        self.robot_arm.robot.plot(trajectory.q)

    def add_configuration(self): 
        joint_values = []
        for p in self.joint_config_entry.params:
            val = p.get()
            val = int(float(val))
            joint_values.append(val)
        self.joint_config_table.joint_table.insert_row(values=joint_values) 
        self.joint_config_table.joint_table.load_table_data()
        self.robot_arm.robot.q = self.to_radians(joint_values)
        for p in self.joint_config_entry.params:
            p.set(str(0))
    
    def show_configuration(self):
        config = self.joint_config_table.joint_table.get_rows(selected=True)
        if len(config) > 1:
            Messagebox.ok(message='Select 1 joint configuration to show')
            return
        config = config[0].values
        old_config = self.robot_arm.robot.q
        self.robot_arm.robot.q = self.to_radians(config)
        self.robot_arm.robot.plot(self.robot_arm.robot.q)
        self.robot_arm.robot.q = old_config

    def add_serial_connection(self, serial):
        self.serial_command_btn = ttk.Button(self, text="Send Serial Command", command=self.send_serial_command)
        self.serial = serial
        self.serial_command_btn.pack(before=self.joint_config_table)
    
    def send_serial_command(self):
        joint_values = self.joint_config_table.joint_table.get_rows(selected=True)
        if len(joint_values) > 1:
            Messagebox.ok(message='Select only 1 joint configuration')
            return
        joint_values = joint_values[0].values
        joint_values = [str(i) for i in joint_values]
        separator = ':'
        serial_msg = f'<{separator.join(joint_values)}>'.encode()
        if not self.serial.is_open:
            self.serial.open()
        self.serial.write(serial_msg)
        data = self.serial.readline()
        print(data.decode('utf-8'))

        