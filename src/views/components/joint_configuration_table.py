import ttkbootstrap as ttkb
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from src.views.components.table_row import TableRow
from src.views.components.button_group import ButtonGroup
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap.constants import GROOVE

class JointConfigurationTable(ttkb.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.joint_entry_frame = ttkb.Frame(self)
        self.joint_table = None
        self.headers = None
        self.name = "joint_table_view"
        self.joint_table_frame = ttkb.Frame(self)
        self.add_to_table_btn = ttkb.Button(self.joint_entry_frame, 
                                            text="Add to table", 
                                            bootstyle="secondary.TButton")

        self.table_btn_group = ButtonGroup(self.joint_table_frame,
                                           [("Add Joint Configuration",),
                                            ("Show Configuration",),
                                            ("Simulate Trajectory",),
                                            ("Send To Robot",),
                                            ("Save Trajectory Data",),
                                            ("Clear table",)],
                                            "default",
                                            horizontal=False,
                                            style="secondary.TButton")

    def create_joint_entries(self, n:int):
        if self.headers or self.joint_table:
            self.headers = None
            self.joint_table.destroy()
            self.joint_table = None
            self.joint_config_entry.destroy()
            self.joint_config_entry = None

        self.headers = [f"Joint{i+1}" for i in range(n)]
        self.joint_table = Tableview(
                self.joint_table_frame,
                coldata=self.headers,
                rowdata=[],
                height=20,
                bootstyle="dark"
                )
        self.joint_table.autofit_columns()
        self.joint_config_entry = TableRow(self.joint_entry_frame, n, "Configure Joints",width=10)
        self.joint_config_entry.pack(pady=(150,0))
        self.add_to_table_btn.pack(anchor="ne")
        self.joint_entry_frame.pack()
        self.table_btn_group.pack(side="left")
        self.joint_table.pack()
        self.joint_table_frame.pack()


    def error_msg(self, msg:str):
        Messagebox.ok(message=msg)

