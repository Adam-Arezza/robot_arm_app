import ttkbootstrap as ttkb
from src.views.components.button_group import ButtonGroup
from ttkbootstrap.dialogs.dialogs import Messagebox
from src.utils import to_degrees, to_radians
from ttkbootstrap.constants import GROOVE
from ttkbootstrap import BooleanVar, StringVar


class Menu(ttkb.Menu):
    def __init__(self, root, config, controller):
        super().__init__(root)
        self.controller = controller
        self.config = config
        self.file_menu = ttkb.Menu(root)
        self.file_menu.add_command(label='Create', command=self.controller.create_robot)
        self.file_menu.add_command(label='Save', command=self.controller.save_robot)
        self.file_menu.add_command(label='Load', command=self.controller.load_robot)
        self.file_menu.add_command(label='Exit', command=self.controller.exit)
        self.add_cascade(label="File", menu=self.file_menu)
        self.add_command(label="Help", command=self.controller.show_help_dialog)
        #self.add_command(label='Create', command=self.controller.create_robot)
        #self.add_command(label='Save', command=self.controller.save_robot)
        #self.add_command(label='Load', command=self.controller.load_robot)
        #self.menu_button_group = ButtonGroup(self,
        #                                          [('Create', self.controller.create_robot),
        #                                            ('Save', self.controller.save_robot),
        #                                            ('Load', self.controller.load_robot),
        #                                            ('Reset', self.controller.reset_robot)],
        #                                           'secondary.TFrame',
        #                                           horizontal=True,
        #                                           style='primary.TButton')
        #self.menu_button_group.pack(fill='x')

