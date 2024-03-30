import ttkbootstrap as ttkb
from src.views.components.button_group import ButtonGroup
from ttkbootstrap.dialogs.dialogs import Messagebox
from src.utils import to_degrees, to_radians
from ttkbootstrap.constants import GROOVE
from ttkbootstrap import BooleanVar, StringVar

class SideMenu(ttkb.Frame):
    def __init__(self, parent, config, controller):
        super().__init__(parent, style='secondary.TFrame')
        self.controller = controller
        self.config = config
        self.style = ttkb.Style()
        self.style.configure('primary.TButton', font=('Helvetica', 11))
        self.side_menu_button_group = ButtonGroup(self,
                                                  [('Create', self.controller.create_robot),
                                                    ('Save', self.controller.save_robot),
                                                    ('Load', self.controller.load_robot),
                                                    ('Reset', self.controller.reset_robot)],
                                                   'secondary.TFrame',
                                                   horizontal=False,
                                                   style='primary.TButton')
        self.side_menu_button_group.pack(fill='x')

#        self.check_btn_frame = ttkb.Frame(self, style='secondary.TFrame')
#
#        self.toggle_label = ttkb.Label(self.check_btn_frame, 
#                                       textvariable=self.mode_string, 
#                                       bootstyle='default')
#
#        self.toggle_mode_switch = ttkb.Checkbutton(self.check_btn_frame,
#                                                   onvalue=True,
#                                                   offvalue=False,
#                                                   variable=self.mode_value,
#                                                   command=self.controller.toggle_auto_manual,
#                                                   bootstyle='default')
#
#        self.toggle_label.pack()
#        self.toggle_mode_switch.pack(padx=10, pady=5)
#        self.check_btn_frame.pack()
#
