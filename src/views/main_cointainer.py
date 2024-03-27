import ttkbootstrap as ttkb
from src.controllers.side_menu_controller import SideMenuController
from src.controllers.robot_controller import RobotController
from src.controllers.start_view_controller import StartViewController
from src.controllers.serial_controller import SerialController
from src.controllers.joint_table_controller import JointTableController
from src.controllers.manual_controller import ManualController
from src.views.components.table_row import TableRow
from src.utils import to_degrees, to_radians
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap.constants import GROOVE
from src.views.robot_view import RobotView


class MainContainer(ttkb.Frame):
    def __init__(self, root):
        super().__init__(root, borderwidth=2, relief=GROOVE, style='danger.TFrame')
        self.root = root
        self.start_controller = StartViewController(root, self)
        self.start_controller.show_view()
        self.side_menu_controller = SideMenuController(root, self)
        self.joint_table_controller = JointTableController(root, self, 4)
        self.manual_controller = ManualController(root, self)
        self.serial_controller = SerialController(root, self, self.joint_table_controller.view.joint_table)
        self.headers = ['Theta (deg)', 'Alpha (deg)', 'r (m)', 'd (m)']    
        

    def main_view(self):
        self.start_controller.kill_view()
        self.side_menu_controller.show_view()
        self.root.robot_controller.show_view()
        self.serial_controller.show_view()
        self.manual_controller.show_view()
        self.joint_table_controller.show_view()
        

    def on_close(self):
        self.root.robot_controller.kill_view()
        self.destroy()

