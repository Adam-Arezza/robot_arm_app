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
        
