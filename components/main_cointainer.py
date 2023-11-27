import ttkbootstrap as ttk
import roboticstoolbox as rtb
from components.robot_config import RobotConfig
from components.table_row import TableRow
from components.joint_config import JointConfig
from components.joint_configuration_table import JointConfigurationTable
from PIL import Image
Image.CUBIC = Image.BICUBIC
from components.serial_connector import SerialConnector
from utils import to_degrees, to_radians
from ttkbootstrap.dialogs.dialogs import Messagebox
from components.robot_view import RobotView

class MainContainer(ttk.Frame):
    def __init__(self, parent, name, robot_arm):
        super().__init__(parent, name=name, width=700)
        self.robot_arm = robot_arm
        self.joint_config_list = []
        self.selected_joint_configurations = []
        self.default_joint_state = self.robot_arm.robot.q

        self.top_frame = ttk.Frame(self)
        self.top_frame.pack(fill='x')
        self.robot_view = RobotView(parent,self.top_frame,self.robot_arm.robot)
        self.robot_view.step()
        self.headers = ['Theta (deg)', 'Alpha (deg)', 'r (m)', 'd (m)']    
        #self.robot_config = RobotConfig(self.top_frame, robot_arm.dh_params, self.headers)
        #self.robot_config.pack(side='left') 

        #self.initial_joint_state = ttk.StringVar()
        #self.previous_joint_state = ttk.StringVar()
        #self.current_joint_state = ttk.StringVar()

        #self.initial_joint_state.set(str(to_degrees(robot_arm.robot.q)))

        #self.initial_joints = JointConfig(self.top_frame, 'Initial Joint State',
        #                                  self.initial_joint_state)
        #self.previous_joints = JointConfig(self.top_frame, 'Previous Joint State',
        #                                   self.previous_joint_state)
        #self.current_joints = JointConfig(self.top_frame, 'Current Joint State',
        #                                  self.current_joint_state)

        #self.initial_joints.pack()
        #self.previous_joints.pack()
        #self.current_joints.pack()

        
        self.serial_connector = SerialConnector(self.top_frame)
        self.serial_connector.pack(pady=(10, 50))
        self.serial_command_btn = ttk.Button(self, text="Send Position", command=self.send_serial_command)

# Joint entry
        self.joint_entry_frame = ttk.Frame(self)
        self.joint_config_entry = TableRow(self.joint_entry_frame, 'Configure Joints')
        self.joint_config_entry.pack(side='left', pady=15)

        self.add_to_table_btn = ttk.Button(self.joint_entry_frame, text='Add to table', command=self.add_configuration, bootstyle='success')
        self.add_to_table_btn.pack(pady=15)

        self.joint_entry_frame.pack(anchor='nw')

#Joint configuration table
        self.joint_config_table = JointConfigurationTable(self, to_degrees(self.robot_arm.robot.q))
        self.joint_config_table.pack(anchor='nw')  

    def add_configuration(self): 
        joint_values = []
        for p in self.joint_config_entry.params:
            val = p.get()
            val = int(float(val))
            joint_values.append(val)
        self.joint_config_table.joint_table.insert_row(values=joint_values) 
        self.joint_config_table.joint_table.load_table_data()
        self.robot_arm.robot.q = to_radians(joint_values)
        for p in self.joint_config_entry.params:
            p.set(str(0)) 

    def add_serial_connection(self, serial):
        self.serial = serial
        self.serial_command_btn.pack(before=self.joint_config_entry, anchor='nw')

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
        self.serial.reset_input_buffer()
        data = self.serial.readline()
        print(data.decode())

