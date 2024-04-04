import ttkbootstrap as ttkb
from src.views.components.button_group import ButtonGroup
from ttkbootstrap.dialogs.dialogs import Messagebox
from src.utils import to_degrees, to_radians
from ttkbootstrap.constants import GROOVE
from ttkbootstrap import BooleanVar, StringVar

class Menu(ttkb.Frame):
    def __init__(self, parent, config, controller):
        super().__init__(parent, style='secondary.TFrame')
        self.controller = controller
        self.config = config
       # self.style = ttkb.Style()
       # self.style.configure('primary.TButton', font=('Helvetica', 15))
        self.menu_button_group = ButtonGroup(self,
                                                  [('Create', self.controller.create_robot),
                                                    ('Save', self.controller.save_robot),
                                                    ('Load', self.controller.load_robot),
                                                    ('Reset', self.controller.reset_robot)],
                                                   'secondary.TFrame',
                                                   horizontal=True,
                                                   style='primary.TButton')
        self.menu_button_group.pack(fill='x')

