import ttkbootstrap as ttkb
from src.serial_service import SerialService
from src.controllers.menu_controller import MenuController
from src.controllers.robot_controller import RobotController
from src.controllers.start_view_controller import StartViewController
from src.controllers.serial_controller import SerialController
from src.controllers.joint_table_controller import JointTableController
from src.views.components.table_row import TableRow
from src.utils import to_degrees, to_radians
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap.constants import GROOVE
from src.views.robot_view import RobotView
from src.views.start_view import StartView
from src.views.serial_view import SerialView
from src.views.components.joint_configuration_table import JointConfigurationTable
from src.views.components.menu import Menu
from src.views.manual_controls_view import ManualControls
from src.views.camera_view import CameraView
from src.layout_manager import LayoutManager


class MainContainer(ttkb.Frame):
    def __init__(self, root):
        super().__init__(root, style='secondary.TFrame')
        self.root = root
        self.serial_service = SerialService()
        self.layout_mgr = LayoutManager()
        self.main_grid_frame = ttkb.Frame(self)
        self.main_grid_frame.columnconfigure(0, weight=1)
        self.main_grid_frame.columnconfigure(1, weight=1)
        self.main_grid_frame.rowconfigure(0, weight=1)
        self.main_grid_frame.rowconfigure(1, weight=1)

        #controllers
        self.start_controller = StartViewController(root)
        self.menu_controller = MenuController(root)
        self.joint_table_controller = JointTableController(root)
        self.serial_controller = SerialController(self.serial_service)
        self.robot_controller = root.robot_controller

        #self.serial_service.register_callback("update_serial_window",self.serial_controller.update_serial_window)
        #self.serial_service.register_callback("update_robot_joints", self.robot_controller.set_joints)

       #views
        self.menu_view = Menu(self.root, {}, self.menu_controller)
        self.joint_table_view = JointConfigurationTable(self.main_grid_frame, self.joint_table_controller)
        self.serial_view = SerialView(self.main_grid_frame, self.serial_controller)
        self.serial_service.add_controller(self.serial_controller)
        self.robot_view = RobotView(root, 
                                    self.main_grid_frame,
                                    self.robot_controller.slider_callback,
                                    self.robot_controller.toggle_auto_manual)
        self.start_view = StartView(self, self.start_controller.create_dh_robot, self.start_controller.load_robot)
        self.camera_view = CameraView(self.main_grid_frame)
        
        #register views with controllers and layout manager
        #self.menu_controller.add_view(self.menu_view)
        self.joint_table_controller.add_view(self.joint_table_view)
        self.serial_controller.add_view(self.serial_view)
        self.start_controller.add_view(self.start_view)
        self.robot_controller.add_view(self.robot_view)
        self.robot_controller.connect_serial_service(self.serial_service)

        #add views to layout manager
        self.layout_mgr.add_view(self.serial_view)
        self.layout_mgr.add_view(self.joint_table_view)
        self.layout_mgr.add_view(self.robot_view)
        self.layout_mgr.add_view(self.camera_view)
        
        #show start page
        self.start_controller.show_view()
                

    def main_view(self):
        self.root.config(menu=self.menu_view)
        num_joints = len(self.root.robot_controller.model.robot.links)
        self.start_controller.kill_view()
        self.main_grid_frame.grid(column=0, row=1, rowspan=2, columnspan=2, sticky="nsew")
        self.layout_mgr.create_grid(2,2)
        self.robot_view.add_controls(num_joints)
        self.joint_table_view.create_joint_entries(num_joints)
        self.root.robot_controller.set_joints(self.root.robot_controller.model.robot.q)
        self.serial_controller.get_port_list()
        self.serial_controller.add_joint_table(self.joint_table_view.joint_table)


    def on_close(self):
        for view in self.layout_mgr.views:
            view.destroy()
        self.root.robot_controller.kill_view()
        self.serial_service.disconnect()
        print("Shutting down...")
        self.destroy()

