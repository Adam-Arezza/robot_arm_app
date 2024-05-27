import ttkbootstrap as ttkb
from src.serial_service import SerialService
from src.controllers.menu_controller import MenuController
from src.controllers.robot_controller import RobotController
from src.controllers.start_view_controller import StartViewController
from src.controllers.serial_controller import SerialController
from src.controllers.joint_table_controller import JointTableController
from src.controllers.controls_controller import ControlsController
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
        self.start_controller = StartViewController(root,self)
        self.menu_controller = MenuController(root)

        #self.camera_view = CameraView(self.main_grid_frame)
        #show start page
        self.start_controller.show_view()
                

    def main_view(self, model):
        self.root.config(menu=self.menu_controller.view)
        self.robot_model = model
        self.add_controllers()
        self.start_controller.kill_view()
        self.initialize_layout_manager()
        num_joints = len(self.robot_model.robot.links)
        self.create_serial_subscriptions()
        self.joint_table_controller.create_joint_entries(num_joints)
        self.robot_controller.set_joints(self.robot_model.robot.q)
        #self.robot_controller.generate_pose_data()


    def create_serial_subscriptions(self):
        self.serial_service.add_subscriber('new_data', self.serial_controller.update_serial_window_received)
        self.serial_service.add_subscriber('new_data', self.robot_controller.update_joint_data)
        self.serial_service.add_subscriber('connected', self.serial_controller.add_serial_connection)
        self.serial_service.add_subscriber('connected', self.joint_table_controller.add_serial_connection)
        self.serial_service.add_subscriber('connected', self.controls_controller.add_serial_connection)
        self.serial_service.add_subscriber('disconnected', self.serial_controller.remove_serial_connection)
        self.serial_service.add_subscriber('disconnected', self.joint_table_controller.remove_serial_connection)
        self.serial_service.add_subscriber('send', self.serial_controller.update_serial_window_sent)


    def add_controllers(self):
        #controllers
        self.robot_controller = RobotController(self.root, 
                                                self.main_grid_frame, 
                                                self.serial_service.send_serial_msg,
                                                self.robot_model)
        self.joint_table_controller = JointTableController(self.root, 
                                                           self.serial_service.send_serial_msg, 
                                                           self.main_grid_frame)
        self.serial_controller = SerialController(self.serial_service, 
                                                  self.main_grid_frame)
        self.controls_controller = ControlsController(self.root, 
                                                      self.main_grid_frame, 
                                                      self.serial_service.send_serial_msg,
                                                      self.robot_model)

    def initialize_layout_manager(self):
        #add views to layout manager
        self.layout_mgr.add_main_grid(self.main_grid_frame)
        self.layout_mgr.add_view(self.serial_controller.view)
        self.layout_mgr.add_view(self.joint_table_controller.view)
        self.layout_mgr.add_view(self.robot_controller.view)
        #self.layout_mgr.add_view(self.camera_view)
        self.layout_mgr.add_view(self.controls_controller.view)
        self.layout_mgr.create_main_grid()
        self.layout_mgr.create_grid()



    def on_close(self):
        for view in self.layout_mgr.views:
            view.destroy()
        self.robot_controller.view.close()
        self.layout_mgr.main_grid.destroy()
        self.serial_service.disconnect()
        print("Shutting down...")
        self.destroy()

