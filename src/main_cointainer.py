import ttkbootstrap as ttk
import roboticstoolbox as rtb
from src.robot_config import RobotConfig
from src.table_row import TableRow
from src.joint_config import JointConfig
from src.joint_configuration_table import JointConfigurationTable
from PIL import Image
Image.CUBIC = Image.BICUBIC
from src.serial_connector import SerialConnector
from utils import to_degrees, to_radians
from ttkbootstrap.dialogs.dialogs import Messagebox


class MainContainer(ttk.Frame):
    def __init__(self, parent, name, robot_arm):
        super().__init__(parent, name=name, width=700)
        self.robot_arm = robot_arm
        self.joint_config_list = []
        self.selected_joint_configurations = []
        self.default_joint_state = self.robot_arm.robot.q

        self.top_frame = ttk.Frame(self)
        self.top_frame.pack(fill='x')
        self.headers = ['Theta (deg)', 'Alpha (deg)', 'r (m)', 'd (m)']    
        self.serial_connector = SerialConnector(self)
        self.serial_connector.pack(pady=(10, 50))
        self.serial_command_btn = ttk.Button(self, text="Send Position", command=self.send_serial_command)

        self.joint_entry_frame = ttk.Frame(self)
        self.joint_config_entry = TableRow(self.joint_entry_frame, 'Configure Joints')
        self.joint_config_entry.pack(side='left', pady=15)

        self.add_to_table_btn = ttk.Button(self.joint_entry_frame, text='Add to table', command=self.add_configuration, bootstyle='success')
        self.add_to_table_btn.pack(pady=15)

        self.joint_entry_frame.pack(anchor='nw')

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
        self.serial_command_btn.pack(before=self.joint_entry_frame,
                                     anchor='nw')

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

