import ttkbootstrap as ttkb
from src.serial_service import SerialService
from src.controllers.menu_controller import MenuController
from src.controllers.robot_controller import RobotController
from src.controllers.start_view_controller import StartViewController
from src.controllers.serial_controller import SerialController
from src.controllers.joint_table_controller import JointTableController
from src.utils import to_degrees, to_radians
from ttkbootstrap.dialogs.dialogs import Messagebox
from src.views.components.joint_configuration_table import JointConfigurationTable
from src.views.camera_view import CameraView
from src.layout_manager import LayoutManager


class MainContainer(ttkb.Frame):
    def __init__(self, root):
        super().__init__(root, style='secondary.TFrame')
        self.root = root
        self.serial_service = SerialService()
        self.layout_mgr = LayoutManager()
        self.main_grid_frame = ttkb.Frame(self)

        #controllers
        self.robot_controller = RobotController(root, self.main_grid_frame, self.serial_service)
        self.start_controller = StartViewController(root, self)
        self.menu_controller = MenuController(root)
        self.joint_table_controller = JointTableController(root, self.serial_service, self.main_grid_frame)
        self.serial_controller = SerialController(self.serial_service, self.main_grid_frame)

       #views
        self.camera_view = CameraView(self.main_grid_frame)
        
        #add views to layout manager
        self.layout_mgr.add_main_grid(self.main_grid_frame)
        self.layout_mgr.add_view(self.serial_controller.view)
        self.layout_mgr.add_view(self.joint_table_controller.view)
        self.layout_mgr.add_view(self.robot_controller.view)
        self.layout_mgr.add_view(self.camera_view)
        
        #show start page
        self.start_controller.show_view()
                

    def main_view(self):
        self.root.config(menu=self.menu_controller.view)
        num_joints = len(self.robot_controller.model.robot.links)
        self.start_controller.kill_view()
        self.layout_mgr.create_main_grid()
        self.layout_mgr.create_grid()
        self.serial_service.add_subscriber('new_data', self.serial_controller.update_serial_window)
        self.serial_service.add_subscriber('new_data', self.robot_controller.update_joint_data)
        self.serial_service.add_subscriber('connected', self.robot_controller.add_serial_connection)
        self.serial_service.add_subscriber('connected', self.serial_controller.add_serial_connection)
        self.serial_service.add_subscriber('disconnected', self.robot_controller.remove_serial_connection)
        self.joint_table_controller.view.create_joint_entries(num_joints)
        self.robot_controller.set_joints(self.robot_controller.model.robot.q)


    def on_close(self):
        for view in self.layout_mgr.views:
            view.destroy()
        self.robot_controller.view.close()
        self.layout_mgr.main_grid.destroy()
        self.serial_service.disconnect()
        print("Shutting down...")
        self.destroy()

