import ttkbootstrap as ttkb
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from src.views.components.table_row import TableRow
from src.views.components.button_group import ButtonGroup
from ttkbootstrap.dialogs.dialogs import Messagebox

class JointConfigurationTable(ttkb.Frame):
    def __init__(self, parent):
        super().__init__(parent, borderwidth=2, relief=GROOVE)
        self.header = ttkb.Label(self, text='Joint Configurator', font=('bold', 12))
        self.joint_entry_frame = ttkb.Frame(self)
        self.joint_table = None
        self.headers = None

        self.add_to_table_btn = ttkb.Button(self.joint_entry_frame, 
                                            text='Add to table', 
                                            bootstyle='primary.Outline.TButton')

        self.table_btn_group = ButtonGroup(self,
                                           [('Add Joint Configuration',),
                                            ('Show Configuration',),
                                            ('Show Trajectory',)],
                                            'default',
                                            horizontal=False,
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
                bootstyle='info', 
                autofit=True
                )
        self.joint_config_entry = TableRow(self.joint_entry_frame, 'Configure Joints', n)
        self.header.pack(anchor='nw')
        self.joint_config_entry.pack(anchor='nw')
        self.add_to_table_btn.pack(anchor='ne',side='right')
        self.joint_entry_frame.pack()
        self.table_btn_group.pack(side='left',padx=(100, 0), pady=10, fill='x', anchor='ne')
        self.joint_table.pack(expand=True, anchor='nw')


    def error_msg(self, msg):
        Messagebox.ok(message=msg)

