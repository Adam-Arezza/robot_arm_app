import ttkbootstrap as ttkb
from src.views.components.button_group import ButtonGroup
from ttkbootstrap.dialogs.dialogs import Messagebox
from src.utils import to_degrees, to_radians
from ttkbootstrap.constants import GROOVE

class SideMenu(ttkb.Frame):
    def __init__(self, parent, config, controller):
        super().__init__(parent, 
                         style='secondary.TFrame', 
                         name='menu_frame',
                         borderwidth=2,
                         relief=GROOVE)
        self.controller = controller
        self.config = config
        self.style = ttkb.Style()
        self.style.configure('info.TButton', font=('Helvetica', 12))

        self.side_menu_button_group = ButtonGroup(self,
                                                  [('Create', self.controller.create_robot),
                                                    ('Save', self.controller.save_robot),
                                                    ('Load', self.controller.load_robot),
                                                    ('Reset', self.controller.reset_robot)],
                                                   'secondary.TFrame',
                                                   horizontal=False,
                                                   style='info.TButton')
        self.side_menu_button_group.pack(fill='x')
        self.toggle_mode_switch = ttkb.Checkbutton(self, text='Mode', style='Roundtoggle.Toolbutton')
        self.toggle_mode_switch.pack()

