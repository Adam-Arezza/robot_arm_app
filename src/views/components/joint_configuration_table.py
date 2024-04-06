import ttkbootstrap as ttkb
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from src.views.components.table_row import TableRow
from src.views.components.button_group import ButtonGroup
from ttkbootstrap.dialogs.dialogs import Messagebox

class JointConfigurationTable(ttkb.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, borderwidth=2, relief=GROOVE)
        self.controller = controller
        self.header = ttkb.Label(self, text='Joint Configurator', font=('bold', 12))
        self.joint_entry_frame = ttkb.Frame(self)
        self.joint_table = None
        self.headers = None

        self.add_to_table_btn = ttkb.Button(self.joint_entry_frame, 
                                            text='Add to table', 
                                            command=self.controller.add_configuration, 
                                            bootstyle='primary.Outline.TButton')

        self.table_btn_group = ButtonGroup(self, [
            ('Add Joint Configuration', self.controller.add_joint_configuration),
            ('Show Configuration', self.controller.show_configuration),
            ('Show Trajectory', self.controller.show_trajectory)],
                                           'default',
                                           horizontal=True,
                                           style='primary.TButton')
        
        

    def create_joint_entries(self, n):
        if self.headers or self.joint_table:
            self.headers = None
            self.joint_table.destroy()
            self.joint_table = None
            self.joint_config_entry.destroy()
            self.joint_config_entry = None

        self.headers = [f'Joint{i}' for i in range(n)]
        self.joint_table = Tableview(
            self,
            coldata=self.headers,
            rowdata=[],
            height=10,
            bootstyle='info' 
        )
        self.joint_config_entry = TableRow(self.joint_entry_frame, 'Configure Joints', n)
        self.header.pack(anchor='nw')
        self.joint_entry_frame.pack()
        self.joint_config_entry.pack(padx=20, pady=15)
        self.add_to_table_btn.pack(pady=5)
        self.table_btn_group.pack(pady=10, fill='x')
        self.joint_table.pack()


    def error_msg(self, msg):
        Messagebox.ok(message=msg)

