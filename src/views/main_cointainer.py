import ttkbootstrap as ttkb
from src.controllers.side_menu_controller import SideMenuController
from src.controllers.robot_controller import RobotController
from src.controllers.start_view_controller import StartViewController
from src.controllers.serial_controller import SerialController
from src.controllers.joint_table_controller import JointTableController
from src.views.components.table_row import TableRow
from src.utils import to_degrees, to_radians
from ttkbootstrap.dialogs.dialogs import Messagebox
from src.layout_manager import LayoutManager
from ttkbootstrap.constants import GROOVE
from src.views.robot_view import RobotView


class MainContainer(ttkb.Frame):
    def __init__(self, root):
        super().__init__(root, borderwidth=2, relief=GROOVE)
        self.root = root
        self.start_controller = StartViewController(root, self)
        self.start_controller.show_view()
        self.side_menu_controller = SideMenuController(root, self)
        self.serial_controller = SerialController(root, self)
        self.joint_table_controller = JointTableController(root, self, 4)
        self.headers = ['Theta (deg)', 'Alpha (deg)', 'r (m)', 'd (m)']    
        self.layout_manager = LayoutManager()        
        

    def main_view(self):
        self.start_controller.kill_view()
        self.side_menu_controller.show_view()
        self.root.robot_controller.show_view()
        self.serial_controller.show_view()
        self.joint_table_controller.show_view()

    def on_close(self):
        #print("closing all the views...")
        #self.side_menu_controller.kill_view()
        #self.serial_controller.disconnect()
        #print("All serial closed")
        #self.joint_table_controller.kill_view()
        #print("joint table closed")
        self.root.robot_controller.kill_view()
        self.destroy()

    def send_serial_command(self):
        joint_values = self.joint_config_table.joint_table.get_rows(selected=True)
        if len(joint_values) > 1:
            Messagebox.ok(message='Select only 1 joint configuration')
            return
        joint_values = joint_values[0].values
        joint_values = [str(i) for i in joint_values]
        separator = ':'
        serial_msg = f'<{separator.join(joint_values)}>'.encode()
        if not self.serial.is_open:
            self.serial.open()
        self.serial.write(serial_msg)
        self.serial.reset_input_buffer()

