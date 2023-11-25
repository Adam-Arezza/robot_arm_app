import ttkbootstrap as ttk
from components.button_group import ButtonGroup
from ttkbootstrap.dialogs.dialogs import Messagebox
import roboticstoolbox as rtb
from utils import to_degrees, to_radians

class SideMenu(ttk.Frame):
    def __init__(self, parent, save_rb, teach_cb, show_cb):
        super().__init__(parent, padding=10, style='secondary.TFrame', name='menu_frame')
        self.parent = parent
        self.main_container = self.parent.main_container
        self.robot_arm = self.parent.robot_arm
        self.default_joint_state = self.robot_arm.robot.q

        # callback functions
        self.save_robot = save_rb     
        self.teach_cb = teach_cb
        self.show_cb = show_cb
        
        #menu buttons  
        self.save_robot_btn = ttk.Button(self, text='Save Robot', width=30, command=self.save_robot) 
        
        self.teach_pendant_btn = ttk.Button(self, text='Teach Pendant', width=30, command=self.teach_cb)

        self.show_robot_btn = ttk.Button(self, text='Show Robot', width=30, command=self.show_cb) 
        
        # button layout
        self.show_robot_btn.pack(side='top', pady=8)
        self.save_robot_btn.pack(side='top', pady=8) 
        self.teach_pendant_btn.pack(side='top', pady=8)


        self.table_btn_group = ButtonGroup(self, [('Update Joints', self.update_joint_configs),
                                                  ('Add Joint Configuration', self.add_joint_configuration),
                                                  ('Show Configuration', self.show_configuration),
                                                  ('Show Trajectory', self.show_trajectory),
                                                  ('Re-initialize', self.set_to_initial_state)],
                                                  'secondary.TFrame',
                                                  horizontal=False,
                                                  style='info')
        self.table_btn_group.pack(pady=25, fill='x')

    def set_to_initial_state(self):
        self.robot_arm.robot.q = self.default_joint_state

    def update_joint_configs(self):
        self.main_container.previous_joint_state.set(self.main_container.current_joint_state.get())
        self.main_container.current_joint_state.set(str(to_degrees(self.robot_arm.robot.q))) 

    def add_joint_configuration(self):
        rows = self.main_container.joint_config_table.joint_table.get_rows(visible=True)
        for row in rows:
            are_equal = all(i == j for i, j in zip(row.values, self.robot_arm.robot.q))
            if are_equal:
                Messagebox.ok(message='The table already has this configuration')
                return 
        self.main_container.joint_config_table.joint_table.insert_row(values=to_degrees(self.robot_arm.robot.q))
        self.main_container.joint_config_table.joint_table.load_table_data()
        self.update_joint_configs()
    
    def show_trajectory(self):
        joint_configurations = self.main_container.joint_config_table.joint_table.get_rows(selected=True)
        if len(joint_configurations) != 2:
            Messagebox.ok(message='Select 2 joint configurations to compute a trajectory')
            return
        row_values = [to_radians(i.values) for i in joint_configurations]
        trajectory = rtb.jtraj(row_values[0], row_values[1], t=25)
        self.robot_arm.robot.plot(trajectory.q)
    
    def show_configuration(self):
        config = self.main_container.joint_config_table.joint_table.get_rows(selected=True)
        if len(config) > 1:
            Messagebox.ok(message='Select 1 joint configuration to show')
            return
        config = config[0].values
        old_config = self.robot_arm.robot.q
        self.robot_arm.robot.q = to_radians(config)
        self.robot_arm.robot.plot(self.robot_arm.robot.q)
        self.robot_arm.robot.q = old_config
