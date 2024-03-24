import ttkbootstrap as ttkb
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from src.views.components.table_row import TableRow
from src.views.components.button_group import ButtonGroup

class JointConfigurationTable(ttkb.Frame):
    def __init__(self, parent, controller, num_joints):
        super().__init__(parent, borderwidth=2, relief=GROOVE)
        self.controller = controller
        self.headers = [f'Joint{i}' for i in range(num_joints)]
        self.joint_table = Tableview(
            self,
            coldata=self.headers,
            rowdata=[],
            height=10,
            bootstyle='light' 
        )

        self.joint_config_entry = TableRow(self, 'Configure Joints')
        self.joint_config_entry.pack(pady=15)
        self.add_to_table_btn = ttkb.Button(self, 
                                            text='Add to table', 
                                            command=self.controller.add_configuration, 
                                            bootstyle='success')
        
        self.table_btn_group = ButtonGroup(self, [
            ('Add Joint Configuration', self.controller.add_joint_configuration),
            ('Show Configuration', self.controller.show_configuration),
            ('Show Trajectory', self.controller.show_trajectory)],
                                           'primary.TFrame',
                                           horizontal=True,
                                           style='info')
         
        self.add_to_table_btn.pack(pady=5)
        self.table_btn_group.pack(pady=25, fill='x')
        self.joint_table.pack()
